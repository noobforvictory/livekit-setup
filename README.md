# LiveKit Learning Stack

Local LiveKit + SIP + Python agent worker.

## Start Everything

```bash
cd /home/denis/livekit-learning
docker compose up -d --build
```

## Make A Real Agent Call

Run this once after starting the stack, or any time the trunk was reset:

```bash
cd /home/denis/livekit-learning/sip/telnyx
./scripts/create-outbound-trunk.py
```

This updates both env files and restarts the agent worker.

Then place the call:

```bash
./scripts/dispatch-agent-call.py
```

## Check Logs

```bash
cd /home/denis/livekit-learning
docker compose logs --tail 80 agent
docker compose logs --tail 80 sip
```

## Debug SIP Traffic

`ngrep` is useful when the logs do not explain a call setup problem. Keep this
running while dispatching a test call to watch SIP requests and responses:

```bash
sudo ngrep -d any -W byline -t 'INVITE|ACK|BYE|CANCEL|REGISTER|OPTIONS|SIP/2.0' 'udp and port 5060'
```

Useful things to check:

- `401` or `403` usually means trunk/auth configuration.
- `404`, `480`, or `486` usually means destination/routing/availability.
- No SIP traffic usually means the request is not reaching the local SIP service.

## Stop Everything

```bash
cd /home/denis/livekit-learning
docker compose down
```

## Terminal Voice Test

This keeps the local microphone/speaker test path separate from the call worker:

```bash
cd /home/denis/livekit-learning
HOST_UID=$(id -u) HOST_GID=$(id -g) docker compose run --rm --build agent-console
```

## Required Env Files

`agent-starter-python/.env.local` needs:

```env
LIVEKIT_URL=ws://localhost:7880
LIVEKIT_API_KEY=devkey
LIVEKIT_API_SECRET=secret
LIVEKIT_AGENT_NAME=my-agent
OPENAI_API_KEY=...
DEEPGRAM_API_KEY=...
AZURE_SPEECH_KEY=...
AZURE_SPEECH_REGION=...
```

`sip/telnyx/.env` needs:

```env
LIVEKIT_URL=http://localhost:7880
LIVEKIT_API_KEY=devkey
LIVEKIT_API_SECRET=secret
LIVEKIT_AGENT_NAME=my-agent
TELNYX_PHONE_NUMBER=+1...
TELNYX_SIP_USERNAME=...
TELNYX_SIP_PASSWORD=...
TELNYX_TEST_DESTINATION=+1...
```
