"""Backward-compatible entry point for the maintained CoCGEC annotator.

Prefer ``cocgec annotate --input ... --output ...`` in new workflows.
"""

from __future__ import annotations

import sys

from cocgec.cli import main


if __name__ == "__main__":
    sys.argv.insert(1, "annotate")
    main()
