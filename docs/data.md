# Data preparation and schema

## Dataset acquisition

The GitHub release includes `data/CoCGEC_train.json`, the paper's derived
training annotations. It does not mirror the original FCGEC or NaCGEC releases.

- FCGEC: <https://github.com/xlxwalex/FCGEC>
- NaCGEC: <https://github.com/masr2000/NaCGEC>

Keep separately downloaded files under `data/raw/`; that directory is ignored by Git. Before
publishing derived annotations or model outputs, verify that the corresponding
upstream license permits redistribution. Code licensing and data licensing are
independent.

## Normalized record

| Field | Type | Meaning |
| --- | --- | --- |
| `id` | string | Stable dataset identifier. |
| `sentence` | string | Original sentence. |
| `corrected_sentence` | array of strings | One or more references. |
| `error_flag` | integer | `1` for an erroneous sentence, otherwise `0`. |
| `error_type` | string | Chinese name or code below. |
| `error_range` | string | Generated source substring; absent for no-error data. |

Legacy aliases (`input`, `output`, `flag`, `type`) are accepted by the package,
but new datasets should use the normalized names. The annotator returns a copy of
each record and preserves unknown metadata.

## Error labels

| Code | Chinese label | English label | Integrated level |
| --- | --- | --- | --- |
| IWO | 语序不当 | Incorrect Word Order | clause |
| IWC | 搭配不当 | Incorrect Word Collocation | clause |
| CM | 成分残缺 | Component Missing | clause |
| CR | 成分赘余 | Component Redundancy | word |
| SC | 结构混乱 | Structure Confusion | clause |
| ILL | 不合逻辑 | Illogicality | clause |
| AM | 表意不明 | Ambiguity | word |

The paper text also uses MS/MR descriptively in one appendix paragraph; the
released FCGEC-compatible code uses `CM` and `CR`, matching the experimental
scripts and table headings.

## Cleaning recommendations

Perform these transformations before annotation and record them in dataset
metadata:

1. decode all files as UTF-8;
2. normalize only the ASCII punctuation explicitly required by the benchmark;
3. deduplicate by a stable identifier or exact original sentence;
4. retain every distinct reference in original order;
5. do not silently discard a reference equal to the source unless the upstream
   annotation specification identifies it as invalid;
6. validate that `error_flag=0` examples contain the source as a reference.

Avoid broad Unicode normalization without measuring its impact: width and
punctuation changes affect character-offset evaluation.

## Generated artifacts

Place generated ranges, instructions, predictions, and submissions under
`data/processed/` or `outputs/`. These locations are ignored by default so that a
public push does not accidentally include licensed data. The synthetic files in
`examples/` are the exception.
