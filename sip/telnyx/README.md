# Telnyx outbound SIP setup

This is the smallest local setup for placing a test call through Telnyx using the local LiveKit server and SIP service.

## What you need from Telnyx

- A Telnyx phone number in `+E.164` format.
- One outbound voice profile.
- One FQDN SIP connection with outbound authentication enabled.
- The SIP username and password from that FQDN connection.
- For a trial account, a verified destination phone number. Telnyx trial voice calls can only dial that verified number.

Telnyx's LiveKit setup docs recommend TCP transport and `sip.telnyx.com` as the basic US SIP signaling address.

## Configure Telnyx

In the Telnyx portal:

1. Verify the personal phone number you want to call during the trial.
2. Buy or assign one Telnyx phone number.
3. Create an outbound voice profile.
4. Create an FQDN SIP connection.
5. Set outbound authentication username and password.
6. Attach the outbound voice profile to the connection.
7. Attach your Telnyx phone number to the connection.

Keep the username and password. Do not commit them.

## Configure this repo

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

For a trial account, `TELNYX_TEST_DESTINATION` must be the verified phone number.

Also add these values to `/home/denis/livekit-learning/agent-starter-python/.env.local` after you create the LiveKit outbound trunk:

```env
LIVEKIT_SIP_OUTBOUND_TRUNK_ID=ST_...
TELNYX_PHONE_NUMBER=+1...
```

## Start local LiveKit and SIP

From the repo root:

```bash
docker compose up -d --build redis livekit-server sip
```

Check:

```bash
docker compose ps
docker compose logs --tail 100 sip
```

## Create the LiveKit outbound trunk

```bash
cd /home/denis/livekit-learning/sip/telnyx
./scripts/create-outbound-trunk.sh
```

Copy the returned `SIPTrunkID` into `.env`:

```env
LIVEKIT_SIP_OUTBOUND_TRUNK_ID=ST_...
```

## Place a test call

For an agent call, first start the Python agent as a LiveKit worker:

```bash
cd /home/denis/livekit-learning/agent-starter-python
uv run python src/agent.py dev
```

Then dispatch the agent and have it dial the verified test number:

```bash
cd /home/denis/livekit-learning/sip/telnyx
./scripts/dispatch-agent-call.sh
```

For a raw SIP-only test without the agent:

```bash
./scripts/call-test-number.sh
```

The raw SIP-only test creates a SIP participant in room `telnyx-test-room` and dials `TELNYX_TEST_DESTINATION` through Telnyx.

## Notes

- Telnyx trial accounts have voice restrictions: outbound calls can only dial your verified phone number, inbound calls must originate from that verified number, and trial calls are time-limited.
- This local setup is best for outbound testing. Inbound calls from Telnyx require your LiveKit SIP service to be reachable from the public internet on SIP and RTP ports.
- If the call connects but there is no audio, check firewall and NAT behavior for UDP RTP ports `10000-20000`.
