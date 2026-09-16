# Contributing

Thank you for improving CoCGEC. Keep changes focused on reproducible CGEC data
preparation and evaluation.

1. Create a branch and install the project with `python -m pip install -e ".[dev]"`.
2. Add or update tests for behavior changes.
3. Run `pytest` and `ruff check .` before opening a pull request.
4. Do not commit benchmark data, model weights, API credentials, or identifiable
   annotation-worker information.
5. Document behavior that can change generated spans or instruction ordering.

Bug reports should include a minimal synthetic record, the command, Python and
package versions, and the observed/expected output. Please do not paste samples
whose dataset license prohibits redistribution.
