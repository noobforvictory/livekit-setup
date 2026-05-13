# LiveKit Learning Stack

This workspace runs a local self-hosted LiveKit stack with SIP and a Python
LiveKit agent.

Services:

- `livekit-server`: local LiveKit server in dev mode.
- `sip`: LiveKit SIP service.
- `agent`: Python voice console agent from `agent-starter-python`.
- `redis`: dedicated Redis for this stack, listening on host port `6380`.

The services use `network_mode: host`, so they share the host network namespace.
That is why the agent can use `LIVEKIT_URL=ws://localhost:7880` from inside its
container.

## Prerequisites

- Docker with Compose.
- Provider keys in `agent-starter-python/.env.local`:
  - `OPENAI_API_KEY`
  - `DEEPGRAM_API_KEY`
  - `AZURE_SPEECH_KEY` plus `AZURE_SPEECH_REGION`, or `AZURE_SPEECH_HOST`

The local LiveKit values should be:

```env
LIVEKIT_URL=ws://localhost:7880
LIVEKIT_API_KEY=devkey
LIVEKIT_API_SECRET=secret
LIVEKIT_AGENT_NAME=my-agent
```

## Start Infra

From the repo root:

```bash
cd /home/denis/livekit-learning
docker compose up -d --build redis livekit-server sip
```

Check status:

```bash
docker compose ps -a
curl -I --max-time 5 http://localhost:7880
```

Expected:

- `redis` is `Up`.
- `livekit-server` is `Up`.
- `sip` is `Up`.
- `curl` returns `HTTP/1.1 200 OK`.

Follow infra logs while developing:

```bash
docker compose logs -f livekit-server sip redis
```

Stop the stack:

```bash
docker compose down
```

## Run Voice Agent In Terminal

The `agent` Compose service runs the intended voice console mode:

```bash
cd /home/denis/livekit-learning
HOST_UID=$(id -u) HOST_GID=$(id -g) docker compose run --rm --build agent
```

The service is in the `voice` Compose profile so it does not start detached
with a plain `docker compose up -d`. Run it explicitly with the command above.

This runs:

```bash
python src/agent.py console
```

Use this command from a terminal attached to your desktop session, because the
container needs access to your microphone, speakers, and user audio socket.

The service mounts:

- `/dev/snd`
- `${XDG_RUNTIME_DIR}` such as `/run/user/1000`

It also sets `PULSE_SERVER` to the user PulseAudio/PipeWire socket.

## Start Infra And Voice Together

If you want one command that starts the infra services first and then opens the
voice console, run:

```bash
cd /home/denis/livekit-learning
docker compose up -d --build redis livekit-server sip
HOST_UID=$(id -u) HOST_GID=$(id -g) docker compose run --rm --build agent
```

## Testing The Agent

Voice test through Compose:

```bash
cd /home/denis/livekit-learning
HOST_UID=$(id -u) HOST_GID=$(id -g) docker compose run --rm --build agent
```

Eval tests:

```bash
cd /home/denis/livekit-learning/agent-starter-python
PYTHONPATH=src uv run --no-sync pytest
```

`--no-sync` is currently useful because this checkout has some root-owned files
inside `agent-starter-python/.venv`. Recreate or fix that virtualenv before
using plain `uv run`.

## Redis Setup

This stack uses a dedicated Redis on host port `6380`:

```yaml
redis:
  image: redis:7-alpine
  network_mode: host
  command: ["redis-server", "--port", "6380"]
```

SIP is configured to use that Redis:

```yaml
redis:
  address: localhost:6380
```

The port is `6380` because another project already uses the default Redis port,
`6379`, on this host. Since these services use `network_mode: host`, container
ports are real host ports. If this Redis tried to use `6379`, it would conflict
with the other project's Redis and exit with `bind: Address in use`.

To inspect the two ports:

```bash
ss -ltnp 'sport = :6379'
ss -ltnp 'sport = :6380'
```

Expected:

- `6379` may be owned by another project.
- `6380` should be owned by this stack after `docker compose up -d`.

## Useful Commands

```bash
HOST_UID=$(id -u) HOST_GID=$(id -g) docker compose run --rm --build agent
docker compose logs --tail 100 livekit-server
docker compose logs --tail 100 sip
docker compose logs --tail 100 redis
docker compose build agent
```
