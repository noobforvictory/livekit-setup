# Telnyx Call Commands

## Configure Once

```bash
cd /home/denis/livekit-learning/sip/telnyx
cp .env.example .env
```

Edit `.env`:

```env
TELNYX_PHONE_NUMBER=+1...
TELNYX_SIP_USERNAME=...
TELNYX_SIP_PASSWORD=...
TELNYX_TEST_DESTINATION=+1...
```

## Start Stack

```bash
cd /home/denis/livekit-learning
docker compose up -d --build redis livekit-server sip agent
```

## Create Or Refresh Trunk

```bash
cd /home/denis/livekit-learning/sip/telnyx
./scripts/create-outbound-trunk.py
```

This writes `LIVEKIT_SIP_OUTBOUND_TRUNK_ID` into both env files and restarts
the agent worker.

## Make Agent Call

```bash
cd /home/denis/livekit-learning/sip/telnyx
./scripts/dispatch-agent-call.py
```

## Raw SIP Test

```bash
cd /home/denis/livekit-learning/sip/telnyx
./scripts/call-test-number.py
```

## Logs

```bash
cd /home/denis/livekit-learning
docker compose logs --tail 80 agent
docker compose logs --tail 80 sip
```

If Telnyx returns `403 Account is disabled D17`, the local stack reached
Telnyx and Telnyx rejected the call.
