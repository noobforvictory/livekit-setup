#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path

from common import TELNYX_DIR, load_env, render_template


def main() -> None:
    if len(sys.argv) != 2:
        raise SystemExit("usage: render-template.py TEMPLATE")

    load_env()
    template_path = Path(sys.argv[1])
    if not template_path.is_absolute():
        template_path = TELNYX_DIR / template_path
    print(render_template(template_path), end="")


if __name__ == "__main__":
    main()
