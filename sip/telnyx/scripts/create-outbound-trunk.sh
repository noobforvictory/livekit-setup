#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/.."

if [ -f .env ]; then
  set -a
  # shellcheck disable=SC1091
  . ./.env
  set +a
fi

tmp=$(mktemp)
trap 'rm -f "$tmp"' EXIT

./scripts/render-template.sh outbound-trunk.template.json > "$tmp"

lk --url "${LIVEKIT_URL:-http://localhost:7880}" \
  --api-key "${LIVEKIT_API_KEY:-devkey}" \
  --api-secret "${LIVEKIT_API_SECRET:-secret}" \
  sip outbound create "$tmp"
