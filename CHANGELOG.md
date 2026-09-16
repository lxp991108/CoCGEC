# Changelog

## Unreleased

### Maintained release workflow

- Reorganized the project as an installable Python package with a `cocgec` CLI.
- Preserved the paper's char-, word-, and clause-level annotation behavior; the
  implementation reproduces all 19,710 published erroneous-record spans.
- Added deterministic two-stage CoTask instruction construction with explicit
  seed, stage ratio, and task order.
- Replaced hard-coded paths and import-time execution with validated CLI inputs.
- Added multi-reference exact-match evaluation and ChERRANT/FCGEC exports.
- Removed random fabrication of FCGEC error types; valid type predictions are now
  required for changed sentences.
- Added synthetic examples, unit tests, full release-data regression testing,
  Python packaging, CI, citation metadata, and English/Chinese documentation.
- Excluded duplicate paper-era scripts with hard-coded paths or side effects;
  their reproducibility-relevant behavior is covered by maintained commands and
  regression tests.
