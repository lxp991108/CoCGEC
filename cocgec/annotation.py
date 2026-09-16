"""Paper-compatible multi-granularity grammatical-error range annotation.

The default behavior is a maintained implementation of the script that created
the released ``CoCGEC_train.json``. It was regression-checked against every one
of the 19,710 erroneous records in that release.
"""

from __future__ import annotations

import re
from collections.abc import Callable, Iterable, Sequence
from typing import Any

PUNCTUATION = "，。？！：；…"
CLAUSE_BOUNDARY = re.compile(r"[，。？！：；]")
OPENING_MARKS = ("“", "‘", "《")
CLOSING_MARKS = ("”", "’", "》")

WORD_LEVEL_TYPES = frozenset({"成分赘余", "表意不明", "CR", "AM"})
CLAUSE_LEVEL_TYPES = frozenset(
    {
        "语序不当",
        "搭配不当",
        "成分残缺",
        "结构混乱",
        "不合逻辑",
        "IWO",
        "IWC",
        "CM",
        "SC",
        "ILL",
    }
)


def _validate_texts(source: str, references: Iterable[str]) -> list[str]:
    if not isinstance(source, str) or not source:
        raise ValueError("source sentence must be a non-empty string")
    values = [reference for reference in references if isinstance(reference, str)]
    if not values:
        raise ValueError("at least one string reference is required")
    return values


def _paper_paired_punctuation(source: str, fragment: str) -> str:
    """Reproduce the paired-punctuation expansion used to build CoCGEC."""

    if not fragment:
        return fragment
    opening_counts = [fragment.count(mark) for mark in OPENING_MARKS]
    closing_counts = [fragment.count(mark) for mark in CLOSING_MARKS]

    needed = ""
    for index, (opening, closing) in enumerate(zip(opening_counts, closing_counts)):
        if opening != closing:
            needed = (
                CLOSING_MARKS[index] if opening > closing else OPENING_MARKS[index]
            )
            break
    if not needed:
        return fragment

    found_pair = False
    if source.startswith(fragment):
        remainder = source[len(fragment) :]
        for char in remainder:
            if not found_pair:
                fragment += char
                found_pair = char == needed
            elif char not in PUNCTUATION:
                fragment += char
            else:
                break
    elif source.endswith(fragment):
        # This slice is intentionally retained for exact compatibility with the
        # released annotation script.
        remainder = list(source[: len(fragment)])
        remainder.reverse()
        for char in remainder:
            if not found_pair:
                fragment = char + fragment
                found_pair = char == needed
            elif char not in PUNCTUATION:
                fragment = char + fragment
            else:
                break
    else:
        parts = source.split(fragment)
        if len(parts) < 2:
            return fragment
        left = list(parts[0])
        left.reverse()
        right = list(parts[1])
        if needed in OPENING_MARKS:
            for char in left:
                if not found_pair:
                    fragment = char + fragment
                    found_pair = char == needed
                elif char not in PUNCTUATION:
                    fragment = char + fragment
                else:
                    break
            for char in right:
                if char not in PUNCTUATION:
                    fragment += char
                else:
                    break
        else:
            for char in left:
                if char not in PUNCTUATION:
                    fragment = char + fragment
                else:
                    break
            for char in right:
                if not found_pair:
                    fragment += char
                    found_pair = char == needed
                elif char not in PUNCTUATION:
                    fragment += char
                else:
                    break

    for opening, closing in zip(OPENING_MARKS, CLOSING_MARKS):
        if fragment.startswith(opening) and fragment.endswith(closing):
            fragment = fragment[1:-1]
    if fragment and fragment[-1] in PUNCTUATION:
        fragment = fragment[:-1]
    return fragment


def _range_from_units(source: str, references: Sequence[str], units: Sequence[str]) -> str:
    indexes: list[int] = []
    for reference in references:
        forward = reference
        backward = reference
        for index, unit in enumerate(units):
            if forward.startswith(unit):
                forward = forward[len(unit) :]
            else:
                indexes.append(index)
                break
        for index in range(len(units) - 1, -1, -1):
            unit = units[index]
            if backward.endswith(unit):
                backward = backward[: len(backward) - len(unit)]
            else:
                indexes.append(index)
                break

    # The historical script assumes erroneous records differ from a reference.
    # Returning an empty range makes the public API safe for identical inputs
    # without changing any released CoCGEC annotation.
    if not indexes:
        return ""
    indexes.sort()
    start, end = indexes[0], indexes[-1]
    if units[start] in PUNCTUATION and units[end] in PUNCTUATION and end - start > 1:
        start += 1
        end -= 1
    if units[start] in PUNCTUATION:
        start += 1
    if units[end] in PUNCTUATION:
        end -= 1
    if start > end:
        return ""
    return _paper_paired_punctuation(source, "".join(units[start : end + 1]))


def char_error_range(source: str, references: Iterable[str]) -> str:
    refs = _validate_texts(source, references)
    return _range_from_units(source, refs, list(source))


def _jieba_tokens(source: str) -> list[str]:
    try:
        import jieba
    except ImportError as exc:  # pragma: no cover - exercised by CLI users
        raise RuntimeError(
            "word-level annotation requires jieba; install the project dependencies"
        ) from exc
    return list(jieba.lcut(source))


def word_error_range(
    source: str,
    references: Iterable[str],
    tokenizer: Callable[[str], Sequence[str]] | None = None,
) -> str:
    refs = _validate_texts(source, references)
    units = list((tokenizer or _jieba_tokens)(source))
    if not units or "".join(units) != source:
        raise ValueError("tokenizer must return non-empty units that reconstruct source")
    return _range_from_units(source, refs, units)


def clause_error_range(source: str, references: Iterable[str]) -> str:
    """Reproduce the clause comparison and trimming used for CoCGEC."""

    refs = _validate_texts(source, references)
    differing_clauses: list[str] = []
    for reference in refs:
        source_clauses = CLAUSE_BOUNDARY.split(source)
        reference_clauses = CLAUSE_BOUNDARY.split(reference)
        # The released algorithm removes one empty segment, rather than all
        # empty segments. This matters for repeated punctuation and references
        # that begin with a delimiter.
        if "" in source_clauses:
            source_clauses.remove("")
        if "" in reference_clauses:
            reference_clauses.remove("")
        for clause in reference_clauses:
            if source_clauses and clause == source_clauses[0]:
                source_clauses.remove(clause)
            else:
                break
        reference_clauses.reverse()
        for clause in reference_clauses:
            if source_clauses and clause == source_clauses[-1]:
                source_clauses.remove(clause)
            else:
                break
        differing_clauses.extend(source_clauses)

    differing = set(differing_clauses)
    source_clauses = CLAUSE_BOUNDARY.split(source)
    if "" in source_clauses:
        source_clauses.remove("")
    fragment = source
    for clause in source_clauses:
        if clause in differing:
            break
        fragment = fragment[len(clause) :]
        if fragment and fragment[0] in PUNCTUATION:
            fragment = fragment[1:]
    for clause in reversed(source_clauses):
        if fragment and fragment[-1] in PUNCTUATION:
            fragment = fragment[:-1]
        if clause in differing:
            break
        fragment = fragment[: -len(clause)]
    return _paper_paired_punctuation(source, fragment)


def error_range(
    source: str,
    references: Iterable[str],
    error_type: str,
    *,
    granularity: str = "auto",
    tokenizer: Callable[[str], Sequence[str]] | None = None,
) -> str:
    """Generate an error range using a level or the paper's type mapping."""

    references = list(references)
    integrated = granularity == "auto"
    if granularity == "auto":
        if error_type in WORD_LEVEL_TYPES:
            granularity = "word"
        elif error_type in CLAUSE_LEVEL_TYPES:
            granularity = "clause"
        else:
            granularity = "char"

    if granularity == "word":
        result = word_error_range(source, references, tokenizer=tokenizer)
    elif granularity == "clause":
        result = clause_error_range(source, references)
    elif granularity == "char":
        result = char_error_range(source, references)
    else:
        raise ValueError("granularity must be one of: auto, char, word, clause")

    # This fallback order is part of the released integrated procedure. A
    # forced granularity remains pure so it can reproduce paper ablations.
    if integrated and not result:
        result = word_error_range(source, references, tokenizer=tokenizer)
    if integrated and not result:
        result = clause_error_range(source, references)
    return result


def annotate_record(record: dict[str, Any], *, granularity: str = "auto") -> dict[str, Any]:
    """Return a copy of one normalized FCGEC record with ``error_range``."""

    result = dict(record)
    flag = result.get("error_flag", result.get("flag"))
    if flag not in (0, 1, False, True):
        raise ValueError("record needs an error_flag (or flag) equal to 0 or 1")
    if not flag:
        # The released corpus leaves this field absent on no-error records.
        result.pop("error_range", None)
        return result

    source = result.get("sentence", result.get("input"))
    references = result.get("corrected_sentence", result.get("output"))
    error_type = result.get("error_type", result.get("type", ""))
    if isinstance(references, str):
        references = [references]
    if not isinstance(references, list):
        raise TypeError("record needs corrected_sentence (or output) as a list")
    result["error_range"] = error_range(
        source, references, error_type, granularity=granularity
    )
    return result


def annotate_records(
    records: Iterable[dict[str, Any]], *, granularity: str = "auto"
) -> list[dict[str, Any]]:
    return [annotate_record(record, granularity=granularity) for record in records]
