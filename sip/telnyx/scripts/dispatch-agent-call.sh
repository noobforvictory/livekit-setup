#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/.."

if [ -f .env ]; then
  set -a
  # shellcheck disable=SC1091
  . ./.env
  set +a
fi

: "${TELNYX_TEST_DESTINATION:?Missing TELNYX_TEST_DESTINATION}"

metadata=$(printf '{"phone_number":"%s"}' "$TELNYX_TEST_DESTINATION")

lk --url "${LIVEKIT_URL:-http://localhost:7880}" \
  --api-key "${LIVEKIT_API_KEY:-devkey}" \
  --api-secret "${LIVEKIT_API_SECRET:-secret}" \
  dispatch create \
  --new-room \
  --agent-name "${LIVEKIT_AGENT_NAME:-my-agent}" \
  --metadata "$metadata"
