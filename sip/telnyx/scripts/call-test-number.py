#!/usr/bin/env python3
from __future__ import annotations

import tempfile
from pathlib import Path

from common import TELNYX_DIR, livekit_cli, load_env, render_template, run


def main() -> None:
    load_env()
    rendered = render_template(TELNYX_DIR / "participant.template.json")

    with tempfile.NamedTemporaryFile("w", delete=False) as tmp:
        tmp.write(rendered)
        tmp_path = tmp.name

    try:
        run([*livekit_cli(), "sip", "participant", "create", tmp_path])
    finally:
        Path(tmp_path).unlink(missing_ok=True)


if __name__ == "__main__":
    main()
