# CoCGEC

[**English**](README.md) | [**中文**](README_ZH.md)

Official data-preparation utilities for **A Chain-of-Task Framework for
Instruction Tuning of LLMs Based on Chinese Grammatical Error Correction**
(COLING 2025).

CoCGEC reduces over-correction by decomposing Chinese grammatical error
correction (CGEC) into three instruction-tuning tasks:

1. grammatical-error range determination;
2. grammatical-error type classification;
3. grammatical error correction.

This repository provides the released `CoCGEC_train.json` annotations and the
paper-specific, reusable code: automatic
multi-granularity range annotation, deterministic CoTask instruction
construction, prediction parsing, and benchmark export. It does not redistribute
the original FCGEC or NaCGEC distributions; obtain them from their official
repositories and follow their licenses.

Paper: [ACL Anthology](https://aclanthology.org/2025.coling-main.577/), pages
8623–8639.

## Installation

Python 3.10 or newer is required.

```bash
python -m venv .venv
# Linux/macOS: source .venv/bin/activate
# Windows PowerShell: .venv\Scripts\Activate.ps1
python -m pip install -e .
```

For development checks:

```bash
python -m pip install -e ".[dev]"
pytest
```

## Quick start

The included sample is synthetic and safe to redistribute. The released CoCGEC
annotations remain available at `data/CoCGEC_train.json` in the GitHub repository.

```bash
# 1. Add the paper's integrated error-range annotation.
cocgec annotate \
  --input examples/sample_fcgec.json \
  --output data/processed/sample_cocgec.json

# 2. Build the 90% correction / 10% Range-Type-Correction curriculum.
cocgec build-instructions \
  --input data/processed/sample_cocgec.json \
  --output data/processed/sample_instructions.json \
  --stage-two-ratio 0.1 \
  --seed 42

# 3. Evaluate generated text (JSONL field: predict).
cocgec evaluate \
  --gold examples/sample_fcgec.json \
  --predictions examples/sample_predictions.jsonl

# 4. Export character-level ChERRANT input.
cocgec export \
  --gold examples/sample_fcgec.json \
  --predictions examples/sample_predictions.jsonl \
  --format cherrant \
  --output outputs/sample_cherrant.txt

# FCGEC JSON additionally reads a predicted type code from `error_type`.
cocgec export \
  --gold examples/sample_fcgec.json \
  --predictions examples/sample_predictions.jsonl \
  --format fcgec \
  --type-key error_type \
  --output outputs/sample_fcgec.json
```

On PowerShell, put a command on one line or replace each trailing `\` with a
backtick.

## Input format

The preferred normalized JSON input is an array of records:

```json
{
  "id": "demo-1",
  "sentence": "在学习中，我们要及时解决和发现存在的问题。",
  "corrected_sentence": ["在学习中，我们要及时发现和解决存在的问题。"],
  "error_flag": 1,
  "error_type": "语序不当"
}
```

For compatibility with the original scripts, the aliases `input`, `output`,
`flag`, and `type` are accepted. See [docs/data.md](docs/data.md) for the schema,
label mapping, and dataset acquisition notes.

## Annotation method

The annotator compares every reference with the original sentence from both
ends. It supports character, Jieba word, and punctuation-delimited clause
granularity. In the integrated setting reported in the paper:

- component redundancy (CR) and ambiguity (AM) use word-level ranges;
- word order (IWO), collocation (IWC), component missing (CM), structure
  confusion (SC), and illogicality (ILL) use clause-level ranges;
- unknown types fall back to character-level ranges.

Use `--granularity char|word|clause` to run a controlled ablation instead.
Automatic spans are heuristic annotations, not gold linguistic analyses; inspect
them when applying the algorithm to a new dataset or domain.

The maintained implementation was checked against all 19,710 erroneous records
in the released CoCGEC training set and reproduced 19,710/19,710 error ranges.

## Reproducing the training setup

The paper uses Qwen1.5-14B-Chat through LLaMA-Factory. The training
hyperparameters reported in the paper are: learning rate `5e-5`, cosine schedule,
warmup ratio `0.003`, global batch size `256`, and one epoch. Inference uses
temperature `0.1`.

`build-instructions` creates the paper's curriculum without depending on a
specific training framework. Its output (`instruction`, `input`, `output`) can be
consumed by LLaMA-Factory or converted for another trainer. Splitting and
multi-reference sampling are deterministic for a given `--seed`.

Full checkpoints and raw benchmark data are intentionally outside this source
repository. See [docs/reproduction.md](docs/reproduction.md) for the boundary
between the release path and paper-only experiments.

## Repository layout

```text
cocgec/       maintained Python package and CLI
data/         released CoCGEC training annotations
tests/        dependency-light unit tests
examples/     synthetic inputs and predictions
docs/         data, reproduction, and release notes
figure/       paper figures
2088_Paper.pdf
Poster.pptx
```

Paper-era one-off scripts with hard-coded paths, import-time execution, or
in-place output writes are intentionally excluded from the public release. Their
reproducibility-relevant behavior is covered by the maintained CLI and tests.

## Tests

The core test suite uses only Python's standard library and can also be run
before installing development extras:

```bash
python -m unittest discover -s tests -v
```

## Citation

Please cite the COLING 2025 paper:

```bibtex
@inproceedings{liu-etal-2025-chain,
    title = "A Chain-of-Task Framework for Instruction Tuning of {LLM}s Based on {C}hinese Grammatical Error Correction",
    author = "Liu, Xinpeng and Xu, Bing and Yang, Muyun and Cao, Hailong and Zhu, Conghui and Zhao, Tiejun and Lu, Wenpeng",
    booktitle = "Proceedings of the 31st International Conference on Computational Linguistics",
    month = jan,
    year = "2025",
    address = "Abu Dhabi, UAE",
    publisher = "Association for Computational Linguistics",
    url = "https://aclanthology.org/2025.coling-main.577/",
    pages = "8623--8639"
}
```

Machine-readable metadata is provided in [CITATION.cff](CITATION.cff).

## Refactoring notes

The release keeps the paper method unchanged while adding a maintainable CLI,
deterministic seeds, validation, tests, packaging, and CI. It also removes
hard-coded paths, import-time file writes, in-place prediction overwrites, and
random FCGEC type fabrication. See [CHANGELOG.md](CHANGELOG.md) for the concise
change list and [docs/reproduction.md](docs/reproduction.md) for compatibility
details.

## License

The source code is licensed under Apache License 2.0, consistent with the paper's
ethics statement. Dataset and model licenses are separate: downloading or using
FCGEC, NaCGEC, Qwen, or derived artifacts does not make them Apache-2.0 by virtue
of this repository. Review each upstream license before redistribution.
