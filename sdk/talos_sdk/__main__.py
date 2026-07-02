"""Allow `python -m talos_sdk ...` as well as the installed `talos` command."""
from __future__ import annotations

from .cli import main

if __name__ == "__main__":
    raise SystemExit(main())
