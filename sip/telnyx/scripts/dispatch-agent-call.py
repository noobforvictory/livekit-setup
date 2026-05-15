#!/usr/bin/env python3
from __future__ import annotations

import json
import os

from common import livekit_cli, load_env, require_env, run


def main() -> None:
    load_env()
    require_env("TELNYX_TEST_DESTINATION")

    metadata = json.dumps({"phone_number": os.environ["TELNYX_TEST_DESTINATION"]})
    run(
        [
            *livekit_cli(),
            "dispatch",
            "create",
            "--new-room",
            "--agent-name",
            os.environ.get("LIVEKIT_AGENT_NAME", "my-agent"),
            "--metadata",
            metadata,
        ]
    )


if __name__ == "__main__":
    main()
