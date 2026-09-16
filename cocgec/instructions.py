"""Deterministic construction of CoTask instruction-tuning records."""

from __future__ import annotations

import random
from collections.abc import Iterable
from typing import Any

from .constants import CORRECTION_PROMPT, RANGE_PROMPT, TYPE_PROMPT

TASKS = ("range", "type", "correction")


def _source(record: dict[str, Any]) -> str:
    value = record.get("sentence", record.get("input"))
    if not isinstance(value, str):
        raise TypeError("record needs sentence (or input) as a string")
    return value


def _references(record: dict[str, Any]) -> list[str]:
    value = record.get("corrected_sentence", record.get("output"))
    if isinstance(value, str):
        value = [value]
    if not isinstance(value, list) or not value or not all(
        isinstance(item, str) for item in value
    ):
        raise ValueError("record needs corrected_sentence (or output) references")
    return value


def instruction_for(
    record: dict[str, Any], task: str, *, rng: random.Random
) -> dict[str, str]:
    source = _source(record)
    flag = bool(record.get("error_flag", record.get("flag", 0)))

    if task == "range":
        answer = record.get("error_range", record.get("range", "")) if flag else ""
        return {
            "instruction": RANGE_PROMPT,
            "input": source,
            "output": f"该句存在语病的地方：{answer or '没有存在语病的地方'}",
        }
    if task == "type":
        answer = record.get("error_type", record.get("type", "无")) if flag else "无"
        return {
            "instruction": TYPE_PROMPT,
            "input": source,
            "output": f"这句话中含有的语病错误类型：{answer}",
        }
    if task == "correction":
        return {
            "instruction": CORRECTION_PROMPT,
            "input": source,
            "output": f"正确的句子：{rng.choice(_references(record))}",
        }
    raise ValueError(f"unknown task {task!r}; choose from {', '.join(TASKS)}")


def build_two_stage(
    records: Iterable[dict[str, Any]],
    *,
    stage_two_ratio: float = 0.1,
    seed: int = 42,
    task_order: tuple[str, ...] = TASKS,
) -> list[dict[str, str]]:
    """Build the paper's 90% correction + 10% R-T-C curriculum.

    Records are shuffled using a local seeded generator. The first stage gets
    correction instructions only; every second-stage sample emits tasks in the
    requested order. Thus a sample never leaks across stages.
    """

    if not 0 <= stage_two_ratio <= 1:
        raise ValueError("stage_two_ratio must be between 0 and 1")
    if not task_order or any(task not in TASKS for task in task_order):
        raise ValueError(f"task_order may contain only: {', '.join(TASKS)}")

    values = list(records)
    rng = random.Random(seed)
    rng.shuffle(values)
    # The paper-era script switches after ceil(N * (1-ratio)) correction-only
    # samples, leaving floor(N * ratio) samples for stage two.
    stage_two_size = int(len(values) * stage_two_ratio)
    split = len(values) - stage_two_size

    instructions = [
        instruction_for(record, "correction", rng=rng) for record in values[:split]
    ]
    for record in values[split:]:
        instructions.extend(
            instruction_for(record, task, rng=rng) for task in task_order
        )
    return instructions
