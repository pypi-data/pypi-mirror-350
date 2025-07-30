#!/usr/bin/env python
"""Sample script demonstrating how to use the Spicy CLI."""

import sys
from pathlib import Path

# Add the parent directory to the path so we can import the package
parent_dir = Path(__file__).parent.parent
sys.path.insert(0, str(parent_dir))

from spicy_cli.main import app  # noqa: E402

if __name__ == "__main__":
    app()
