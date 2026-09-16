"""Prediction parsing and benchmark export helpers."""

from __future__ import annotations

import re
from typing import Any

from .constants import ERROR_TYPE_NAMES

NO_ERROR_MARKERS = (
    "没有语病",
    "无错误",
    "无语法错误",
    "原句正确",
    "没有语法错误",
    "没有错误",
    "无需修改",
    "无需改正",
    "无需改动",
    "未发现语法错误",
)

ANSWER_PREFIX = re.compile(
    r"^(?:正确的句子(?:是)?|修改后的句子|改正后的句子|输出)\s*[：:]\s*"
)


def parse_prediction(source: str, prediction: str) -> str:
    """Extract one corrected sentence without changing legitimate whitespace."""

    if not isinstance(prediction, str):
        raise TypeError("prediction must be a string")
    value = prediction.strip()
    if not value or any(marker in value for marker in NO_ERROR_MARKERS):
        return source

    candidates = [line.strip() for line in value.splitlines() if line.strip()]
    labelled = [candidate for candidate in candidates if ANSWER_PREFIX.match(candidate)]
    if labelled:
        return ANSWER_PREFIX.sub("", labelled[-1]).strip().strip('"“”')

    for candidate in candidates:
        cleaned = candidate.removeprefix("Assistant:").strip().strip('"“”')
        if cleaned and cleaned != "Human:":
            return cleaned
    return source


def exact_match(
    gold_records: list[dict[str, Any]], predictions: list[str]
) -> dict[str, float | int]:
    if len(gold_records) != len(predictions):
        raise ValueError(
            f"length mismatch: {len(gold_records)} gold records and "
            f"{len(predictions)} predictions"
        )
    correct = 0
    for record, prediction in zip(gold_records, predictions):
        references = record.get("corrected_sentence", record.get("output", []))
        if isinstance(references, str):
            references = [references]
        correct += prediction in references
    total = len(gold_records)
    return {"correct": correct, "total": total, "exact_match": correct / total if total else 0.0}


def to_cherrant_lines(sources: list[str], predictions: list[str]) -> list[str]:
    if len(sources) != len(predictions):
        raise ValueError("sources and predictions must have the same length")
    return [
        f"{index}\t{source}\t{prediction}"
        for index, (source, prediction) in enumerate(
            zip(sources, predictions), start=1
        )
    ]


def to_fcgec_submission(
    gold_records: list[dict[str, Any]],
    predictions: list[str],
    error_types: list[str] | None = None,
) -> dict[str, dict[str, Any]]:
    """Create FCGEC CodaLab JSON without fabricating an error type.

    FCGEC requires one of seven type codes for changed sentences. A
    correction-only model cannot infer it reliably, so callers must provide
    classification predictions instead of assigning a random label.
    """

    if len(gold_records) != len(predictions):
        raise ValueError("gold records and predictions must have the same length")
    if error_types is not None and len(error_types) != len(predictions):
        raise ValueError("error types and predictions must have the same length")
    output: dict[str, dict[str, Any]] = {}
    for index, (record, prediction) in enumerate(zip(gold_records, predictions)):
        source = record.get("sentence", record.get("input"))
        identifier = str(record.get("id", index))
        changed = prediction != source
        if changed:
            if error_types is None:
                raise ValueError(
                    "FCGEC export needs predicted error types for changed sentences"
                )
            error_type = error_types[index]
            if error_type not in ERROR_TYPE_NAMES:
                raise ValueError(
                    f"record {identifier}: expected an FCGEC type code, got {error_type!r}"
                )
        else:
            error_type = "*"
        output[identifier] = {
            "error_flag": int(changed),
            "error_type": error_type,
            "correction": prediction,
        }
    return output
