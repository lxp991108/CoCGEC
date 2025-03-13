"""
Script for identifying error ranges in Chinese sentences through character, word, and clause level analysis.
Converts FCGEC format data to CoCGEC format with error range annotations.
"""

import json
import re
from typing import List, Dict, Any
import jieba
from tqdm import tqdm

# Constants
PUNCTUATION_MARKS = "，。？！：；…"
PAIRED_PUNCTUATIONS = {"“": "”", "‘": "’", "《": "》", "”": "“", "’": "‘", "》": "《"}


def fix_unpaired_punctuation(original: str, fragment: str) -> str:
    """
    Fix unpaired punctuation marks in the identified error fragment by expanding
    the selection from the original sentence.

    Args:
        original: Original complete sentence
        fragment: Identified error fragment with potential unpaired punctuation

    Returns:
        Adjusted fragment with properly paired punctuation
    """
    # Count missing punctuation pairs
    balance = {char: 0 for char in PAIRED_PUNCTUATIONS}
    for char in fragment:
        if char in PAIRED_PUNCTUATIONS:
            balance[char] += 1
        if char in PAIRED_PUNCTUATIONS.values():
            balance[PAIRED_PUNCTUATIONS[char]] -= 1

    # Find first unpaired punctuation
    for char, count in balance.items():
        if count != 0:
            missing_char = PAIRED_PUNCTUATIONS[char] if count > 0 else char
            if missing_char in "“‘《":
                direction = "start"
            else:
                direction = "end"
            fragment = expand_to_match(original, fragment, missing_char, direction)
            if (
                fragment[0] in PAIRED_PUNCTUATIONS
                and fragment[-1] in PAIRED_PUNCTUATIONS
            ):
                fragment = fragment[1:-1]
            return fragment

    return fragment


def expand_to_match(
    original: str, fragment: str, target_char: str, direction: str
) -> str:
    """
    Expand fragment boundaries to include missing punctuation character.

    Args:
        original: Original complete sentence
        fragment: Current error fragment
        target_char: Character to search for
        direction: 'start' or 'end' indicating search direction

    Returns:
        Adjusted fragment with target character included
    """
    if fragment not in original:
        return fragment

    start_idx = (
        original.index(fragment) if direction == "start" else original.rindex(fragment)
    )
    search_range = (
        original[:start_idx][::-1]
        if direction == "start"
        else original[start_idx + len(fragment) :]
    )

    for i, char in enumerate(search_range):
        if char == target_char:
            if direction == "start":
                return original[start_idx - i - 1 : start_idx + len(fragment)]
            else:
                return original[start_idx : start_idx + len(fragment) + i + 1]

    return fragment


def char_level_error_range(entry: Dict[str, Any]) -> str:
    """
    Identify error range at character level through forward/backward matching.

    Args:
        entry: Data entry containing original and corrected sentences

    Returns:
        Identified error range string
    """
    original_chars = list(entry["sentence"])
    indices = []

    for corrected in entry["corrected_sentence"]:
        # Forward matching
        temp = corrected
        for i, char in enumerate(original_chars):
            if temp.startswith(char):
                temp = temp[len(char) :]
            else:
                indices.append(i)
                break

        # Backward matching
        temp = corrected
        for i, char in enumerate(reversed(original_chars)):
            if temp.endswith(char):
                temp = temp[: -len(char)]
            else:
                indices.append(len(original_chars) - 1 - i)
                break

    start = max(min(indices), 0)
    end = min(max(indices), len(original_chars) - 1)

    # Adjust boundaries for punctuation
    while start <= end and original_chars[start] in PUNCTUATION_MARKS:
        start += 1
    while end >= start and original_chars[end] in PUNCTUATION_MARKS:
        end -= 1

    error_fragment = "".join(original_chars[start : end + 1])
    return fix_unpaired_punctuation(entry["sentence"], error_fragment)


def word_level_error_range(entry: Dict[str, Any]) -> str:
    """
    Identify error range at word level using Jieba segmentation.

    Args:
        entry: Data entry containing original and corrected sentences

    Returns:
        Identified error range string
    """
    original_words = jieba.lcut(entry["sentence"])
    indices = []

    for corrected in entry["corrected_sentence"]:
        # Forward matching
        temp = corrected
        for i, word in enumerate(original_words):
            if temp.startswith(word):
                temp = temp[len(word) :]
            else:
                indices.append(i)
                break

        # Backward matching
        temp = corrected
        for i, word in enumerate(reversed(original_words)):
            if temp.endswith(word):
                temp = temp[: -len(word)]
            else:
                indices.append(len(original_words) - 1 - i)
                break

    start = max(min(indices), 0)
    end = min(max(indices), len(original_words) - 1)

    # Adjust boundaries for punctuation
    while start <= end and original_words[start] in PUNCTUATION_MARKS:
        start += 1
    while end >= start and original_words[end] in PUNCTUATION_MARKS:
        end -= 1

    error_fragment = "".join(original_words[start : end + 1])
    return fix_unpaired_punctuation(entry["sentence"], error_fragment)


def clause_level_error_range(entry: Dict[str, Any]) -> str:
    """
    Identify error range at clause level using punctuation boundaries.

    Args:
        entry: Data entry containing original and corrected sentences

    Returns:
        Identified error range string
    """
    clause_split_re = re.compile(r"[，。？！：；]")
    error_clauses = []

    for corrected in entry["corrected_sentence"]:
        original_clauses = [c for c in clause_split_re.split(entry["sentence"]) if c]
        corrected_clauses = [c for c in clause_split_re.split(corrected) if c]

        # Remove matching clauses from both ends
        while (
            original_clauses
            and corrected_clauses
            and original_clauses[0] == corrected_clauses[0]
        ):
            original_clauses.pop(0)
            corrected_clauses.pop(0)

        while (
            original_clauses
            and corrected_clauses
            and original_clauses[-1] == corrected_clauses[-1]
        ):
            original_clauses.pop()
            corrected_clauses.pop()

        error_clauses.extend(original_clauses)

    error_clauses = list(set(error_clauses))
    original, error_fragment = entry["sentence"], entry["sentence"]
    original_clauses = [c for c in clause_split_re.split(original) if c]

    # Trim original sentence based on error clauses
    if "" in original_clauses:
        original_clauses.remove("")

    for clause in original_clauses:
        if clause not in error_clauses:
            error_fragment = error_fragment[len(clause) :]
            if error_fragment[0] in PUNCTUATION_MARKS:
                error_fragment = error_fragment[1:]
        else:
            break

    original_clauses.reverse()
    for clause in original_clauses:
        if error_fragment[-1] in PUNCTUATION_MARKS:
            error_fragment = error_fragment[:-1]
        if clause not in error_clauses:
            error_fragment = error_fragment[: -len(clause)]
        else:
            break

    original_clauses.reverse()
    return fix_unpaired_punctuation(original, error_fragment)


ERROR_TYPE_MAPPING = {
    "表意不明": word_level_error_range,
    "成分赘余": word_level_error_range,
    "语序不当": clause_level_error_range,
    "搭配不当": clause_level_error_range,
    "成分残缺": clause_level_error_range,
    "结构混乱": clause_level_error_range,
    "不合逻辑": clause_level_error_range,
}


def process_dataset(input_path: str, output_path: str) -> None:
    """
    Process dataset file and save results with error ranges.

    Args:
        input_path: Path to input JSON file
        output_path: Path to output JSON file
    """
    with open(input_path, "r", encoding="utf-8") as f:
        dataset = json.load(f)

    for entry in tqdm(dataset, desc="Processing entries"):
        if entry["error_flag"] != 1:
            continue
        processor = ERROR_TYPE_MAPPING.get(entry["error_type"], char_level_error_range)
        entry["error_range"] = processor(entry)

        # Fallback strategy
        if not entry["error_range"]:
            entry["error_range"] = word_level_error_range(
                entry
            ) or clause_level_error_range(entry)

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(dataset, f, indent=2, ensure_ascii=False)


if __name__ == "__main__":
    process_dataset(
        input_path=r"data\FCGEC_train.json",
        output_path=r"data\CoCGEC_train.json",
    )
