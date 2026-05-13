#!/usr/bin/env bash
set -euo pipefail

template="$1"

required_vars=$(grep -o '\${[A-Z0-9_]*}' "$template" | tr -d '${}' | sort -u)
for name in $required_vars; do
  if [ -z "${!name:-}" ]; then
    echo "Missing required environment variable: $name" >&2
    exit 1
  fi
done

envsubst < "$template"
