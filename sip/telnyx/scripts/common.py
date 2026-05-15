#!/usr/bin/env python3
from __future__ import annotations

import os
import re
import subprocess
import sys
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parent
TELNYX_DIR = SCRIPT_DIR.parent
REPO_ROOT = TELNYX_DIR.parent.parent
AGENT_ENV = REPO_ROOT / "agent-starter-python" / ".env.local"
TELNYX_ENV = TELNYX_DIR / ".env"


def load_env(path: Path = TELNYX_ENV) -> None:
    if not path.exists():
        return

    for raw_line in path.read_text().splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("export "):
            line = line[len("export ") :].strip()
        if "=" not in line:
            continue

        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip()

        if (
            len(value) >= 2
            and value[0] == value[-1]
            and value[0] in {"'", '"'}
        ):
            value = value[1:-1]

        os.environ[key] = value


def require_env(*names: str) -> None:
    missing = [name for name in names if not os.environ.get(name)]
    if missing:
        print(
            "Missing required environment variable: " + ", ".join(missing),
            file=sys.stderr,
        )
        raise SystemExit(1)


def livekit_cli() -> list[str]:
    return [
        "lk",
        "--url",
        os.environ.get("LIVEKIT_URL", "http://localhost:7880"),
        "--api-key",
        os.environ.get("LIVEKIT_API_KEY", "devkey"),
        "--api-secret",
        os.environ.get("LIVEKIT_API_SECRET", "secret"),
    ]


def render_template(template_path: Path) -> str:
    template = template_path.read_text()
    names = sorted(set(re.findall(r"\$\{([A-Z0-9_]+)\}", template)))
    require_env(*names)

    def replace(match: re.Match[str]) -> str:
        return os.environ[match.group(1)]

    return re.sub(r"\$\{([A-Z0-9_]+)\}", replace, template)


def run(args: list[str], cwd: Path = TELNYX_DIR) -> None:
    proc = subprocess.run(args, cwd=cwd)
    if proc.returncode:
        raise SystemExit(proc.returncode)


def run_capture(args: list[str], cwd: Path = TELNYX_DIR) -> str:
    proc = subprocess.run(
        args,
        cwd=cwd,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
    )
    print(proc.stdout, end="", flush=True)
    if proc.returncode:
        raise SystemExit(proc.returncode)
    return proc.stdout


def set_env_value(path: Path, key: str, value: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    lines = path.read_text().splitlines() if path.exists() else []
    output: list[str] = []
    written = False

    for line in lines:
        if line.startswith(f"{key}=") or line.startswith(f"export {key}="):
            if not written:
                output.append(f"{key}={value}")
                written = True
            continue
        output.append(line)

    if not written:
        output.append(f"{key}={value}")

    path.write_text("\n".join(output) + "\n")
