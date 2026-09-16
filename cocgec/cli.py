"""Command-line interface for reproducible data preparation."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from .annotation import annotate_records
from .evaluation import (
    exact_match,
    parse_prediction,
    to_cherrant_lines,
    to_fcgec_submission,
)
from .instructions import TASKS, build_two_stage
from .io import read_json, read_jsonl, write_json


def _records(path: str) -> list[dict[str, Any]]:
    value = read_json(path)
    if not isinstance(value, list) or not all(isinstance(item, dict) for item in value):
        raise ValueError(f"{path}: expected a JSON array of objects")
    return value


def _prediction_rows(path: str) -> list[dict[str, Any]]:
    return read_jsonl(path) if Path(path).suffix.lower() == ".jsonl" else _records(path)


def _parsed_predictions(
    gold: list[dict[str, Any]], rows: list[dict[str, Any]], key: str
) -> list[str]:
    if len(gold) != len(rows):
        raise ValueError(f"length mismatch: {len(gold)} gold records and {len(rows)} predictions")
    values = []
    for index, (record, row) in enumerate(zip(gold, rows)):
        if key not in row:
            raise ValueError(f"prediction {index} has no {key!r} field")
        source = record.get("sentence", record.get("input"))
        values.append(parse_prediction(source, row[key]))
    return values


def _annotate(args: argparse.Namespace) -> None:
    write_json(annotate_records(_records(args.input), granularity=args.granularity), args.output)


def _build(args: argparse.Namespace) -> None:
    order = tuple(args.order.split("-"))
    write_json(
        build_two_stage(
            _records(args.input),
            stage_two_ratio=args.stage_two_ratio,
            seed=args.seed,
            task_order=order,
        ),
        args.output,
    )


def _evaluate(args: argparse.Namespace) -> None:
    gold = _records(args.gold)
    predictions = _parsed_predictions(gold, _prediction_rows(args.predictions), args.key)
    print(json.dumps(exact_match(gold, predictions), ensure_ascii=False, indent=2))


def _export(args: argparse.Namespace) -> None:
    gold = _records(args.gold)
    rows = _prediction_rows(args.predictions)
    predictions = _parsed_predictions(gold, rows, args.key)
    target = Path(args.output)
    target.parent.mkdir(parents=True, exist_ok=True)
    if args.format == "cherrant":
        sources = [record.get("sentence", record.get("input")) for record in gold]
        target.write_text("\n".join(to_cherrant_lines(sources, predictions)) + "\n", encoding="utf-8")
    else:
        error_types = []
        for index, row in enumerate(rows):
            if args.type_key not in row:
                raise ValueError(
                    f"prediction {index} has no {args.type_key!r} field required by FCGEC"
                )
            error_types.append(row[args.type_key])
        write_json(to_fcgec_submission(gold, predictions, error_types), target)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="cocgec", description="CoCGEC data preparation and evaluation tools"
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    annotate = subparsers.add_parser("annotate", help="add automatic error ranges")
    annotate.add_argument("--input", required=True, help="normalized FCGEC JSON")
    annotate.add_argument("--output", required=True)
    annotate.add_argument(
        "--granularity",
        choices=("auto", "char", "word", "clause"),
        default="auto",
    )
    annotate.set_defaults(run=_annotate)

    build = subparsers.add_parser("build-instructions", help="build the two-stage curriculum")
    build.add_argument("--input", required=True, help="annotated CoCGEC JSON")
    build.add_argument("--output", required=True)
    build.add_argument("--stage-two-ratio", type=float, default=0.1)
    build.add_argument("--seed", type=int, default=42)
    build.add_argument(
        "--order",
        default="range-type-correction",
        help=f"hyphen-separated tasks chosen from {', '.join(TASKS)}",
    )
    build.set_defaults(run=_build)

    evaluate = subparsers.add_parser("evaluate", help="compute multi-reference exact match")
    evaluate.add_argument("--gold", required=True)
    evaluate.add_argument("--predictions", required=True)
    evaluate.add_argument("--key", default="predict", help="prediction text field")
    evaluate.set_defaults(run=_evaluate)

    export = subparsers.add_parser("export", help="export benchmark submission formats")
    export.add_argument("--gold", required=True)
    export.add_argument("--predictions", required=True)
    export.add_argument("--output", required=True)
    export.add_argument("--key", default="predict", help="prediction text field")
    export.add_argument(
        "--type-key",
        default="error_type",
        help="FCGEC error-type field (IWO/IWC/CM/CR/SC/ILL/AM)",
    )
    export.add_argument("--format", choices=("cherrant", "fcgec"), required=True)
    export.set_defaults(run=_export)
    return parser


def main() -> None:
    args = build_parser().parse_args()
    try:
        args.run(args)
    except (OSError, TypeError, ValueError, json.JSONDecodeError) as exc:
        raise SystemExit(f"error: {exc}") from exc


if __name__ == "__main__":
    main()
