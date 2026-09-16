# Reproduction and code-release policy

## Maintained path

The supported release workflow is:

```text
official dataset -> normalized JSON -> automatic ranges -> CoTask instructions
                 -> external trainer -> parsed predictions -> benchmark format
```

The `cocgec` package implements every paper-specific data transformation in this
workflow. Model fine-tuning remains delegated to LLaMA-Factory, as in the paper,
rather than vendoring a second training framework.

The automatic range implementation was regression-tested against the released
CoCGEC corpus: all 19,710 records with `error_flag=1` reproduce the published
`error_range` exactly. The paper-era `addRange.py`, rather than the later
documentation rewrite named `addErrorRange.py`, is the provenance reference for
these released spans.

## Paper setup

- Base model: Qwen1.5-14B-Chat
- Framework: LLaMA-Factory
- Stage 1: correction instructions from 90% of CoCGEC
- Stage 2: range, type, and correction instructions from the remaining 10%
- Task order: Range -> Type -> Correction
- Initial learning rate: `5e-5`
- Scheduler: cosine
- Warmup ratio: `0.003`
- Global batch size: `256`
- Epochs: `1`
- Inference temperature: `0.1`
- Evaluation: ChERRANT for character-level span correction; official CodaLab
  submission for FCGEC

The seed was not documented in the paper-era scripts. This release defaults to
`42` and records it at the command line; an exact historical shuffle cannot be
claimed without the original shuffled artifact.

## What belongs in the public repository?

| Asset | Release decision | Reason |
| --- | --- | --- |
| Range annotation | Maintained | Central contribution and needed to rebuild CoCGEC. |
| Instruction construction | Maintained | Central CoTask/two-stage contribution. |
| Output parsing and exports | Maintained | Needed for benchmark reproduction. |
| EM/MED annotation analysis | Keep as experiment | Supports the granularity choice in the paper. |
| Task-order/ratio ablations | Keep as experiment | Supports paper ablations, but is not the default API. |
| Temporary print/debug probes | Exclude | No reproducibility value. |
| Released `CoCGEC_train.json` | Keep | Paper artifact already released by the authors. |
| Original FCGEC/NaCGEC distributions | Do not mirror | Link to the upstream repositories. |
| Checkpoints and bulk predictions | Host as release artifacts if permitted | Too large/noisy for source history. |

## Legacy research scripts

One-off paper-era scripts are not part of the public source release. They used
hard-coded local paths, import-time side effects, in-place prediction writes, and
in one case random CodaLab type assignment. The public package replaces all
reproducibility-relevant behavior with validated commands. The historical range
implementation was audited locally against the release artifact, and the public
test suite now enforces exact equality for all published error spans.

## Reproducibility checklist

For each published run, record:

- source dataset version/checksum and its license;
- normalization command and package version;
- `cocgec annotate` granularity;
- `cocgec build-instructions` seed, ratio, and order;
- base model revision and tokenizer revision;
- full LLaMA-Factory configuration and software versions;
- hardware, precision mode, and distributed strategy;
- decoding parameters;
- ChERRANT version/commit and benchmark submission file checksum.
