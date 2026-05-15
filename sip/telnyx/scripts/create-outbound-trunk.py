#!/usr/bin/env python3
from __future__ import annotations

import re
import os
import tempfile
from pathlib import Path

from common import (
    AGENT_ENV,
    REPO_ROOT,
    TELNYX_DIR,
    TELNYX_ENV,
    livekit_cli,
    load_env,
    render_template,
    run,
    run_capture,
    set_env_value,
)


def main() -> None:
    load_env()
    rendered = render_template(TELNYX_DIR / "outbound-trunk.template.json")

    with tempfile.NamedTemporaryFile("w", delete=False) as tmp:
        tmp.write(rendered)
        tmp_path = tmp.name

    try:
        output = run_capture([*livekit_cli(), "sip", "outbound", "create", tmp_path])
    finally:
        Path(tmp_path).unlink(missing_ok=True)

    match = re.search(r"SIPTrunkID:\s*(\S+)", output)
    if not match:
        raise SystemExit("Could not find SIPTrunkID in lk output")

    trunk_id = match.group(1)
    set_env_value(TELNYX_ENV, "LIVEKIT_SIP_OUTBOUND_TRUNK_ID", trunk_id)
    set_env_value(AGENT_ENV, "LIVEKIT_SIP_OUTBOUND_TRUNK_ID", trunk_id)
    set_env_value(AGENT_ENV, "TELNYX_PHONE_NUMBER", os.environ["TELNYX_PHONE_NUMBER"])

    print(
        "Updated trunk ID in sip/telnyx/.env and agent-starter-python/.env.local",
        flush=True,
    )
    print("Restarting agent worker so it loads the new trunk ID...", flush=True)
    run(["docker", "compose", "up", "-d", "--force-recreate", "agent"], cwd=REPO_ROOT)


if __name__ == "__main__":
    main()
