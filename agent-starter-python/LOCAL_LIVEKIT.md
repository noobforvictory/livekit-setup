# Local LiveKit Voice Bot Runbook

This checkout is configured for the local self-hosted LiveKit server in the parent directory. It uses:

- LiveKit server: local `livekit-server --dev`
- LLM: OpenAI normal API
- STT: Deepgram
- TTS: Azure Speech
- Turn handling: local Silero VAD

## 1. Configure Provider Keys

Edit `.env.local` in this directory:

```env
LIVEKIT_URL=ws://localhost:7880
LIVEKIT_API_KEY=devkey
LIVEKIT_API_SECRET=secret
LIVEKIT_AGENT_NAME=my-agent

OPENAI_API_KEY=your-openai-key
OPENAI_MODEL=gpt-4.1-mini

DEEPGRAM_API_KEY=your-deepgram-key
DEEPGRAM_MODEL=nova-3
DEEPGRAM_LANGUAGE=en

AZURE_SPEECH_KEY=your-azure-speech-key
AZURE_SPEECH_REGION=your-azure-region
AZURE_TTS_VOICE=en-US-JennyNeural
AZURE_TTS_LANGUAGE=en-US
```

If Azure uses a host endpoint instead of key plus region, set `AZURE_SPEECH_HOST`.

## 2. Install Dependencies

```bash
cd /home/denis/livekit-learning/agent-starter-python
uv sync
uv run python src/agent.py download-files
```

## 3. Fastest Voice Test

This uses your local microphone and speaker. It does not need the local LiveKit server.

```bash
cd /home/denis/livekit-learning/agent-starter-python
uv run python src/agent.py console
```

If you want to test the LLM path without microphone/audio devices:

```bash
uv run python src/agent.py console --text
```

Say or type a short prompt. If OpenAI quota is available, the agent should answer and Azure Speech should synthesize audio in voice mode.

## 4. Full Local LiveKit Server Mode

The root Compose stack now includes the agent service. Start the local LiveKit stack from the parent directory:

```bash
cd /home/denis/livekit-learning
docker compose up -d --build
```

Use `--no-build` if Docker Hub DNS is flaky and all images are already cached locally:

```bash
docker compose up -d --no-build
```

Confirm LiveKit is up:

```bash
curl -I --max-time 5 http://localhost:7880
docker compose ps
```

Expected running services include:

```text
redis
livekit-server
sip
agent
```

The agent should log that it registered with the local server:

```bash
docker compose logs --tail 100 agent
```

Expected log line:

```text
registered worker {"agent_name": "my-agent", "url": "ws://localhost:7880"}
```

You can still run the agent outside Compose for faster debugging:

```bash
cd /home/denis/livekit-learning/agent-starter-python
uv run python src/agent.py dev
```

## 5. Current Known Blocker

During the last test, Deepgram and Azure worked, and the agent registered with local LiveKit. OpenAI returned:

```text
429 insufficient_quota
```

That means the OpenAI key is accepted syntactically, but the OpenAI project/account has no usable quota or billing. Fix billing/quota or use a key from a project with available quota, then rerun:

```bash
uv run python src/agent.py console --text
```

## Useful Debug Commands

```bash
docker compose logs --tail 100 livekit-server
docker compose logs --tail 100 sip
uv run python src/agent.py --help
uv run ruff check .
uv run pytest
```
