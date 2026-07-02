#!/usr/bin/env bash
# Quick check: confirms your Talos key and the gateway work before launching
# claude.
set -euo pipefail

: "${TALOS_API_KEY:?Set TALOS_API_KEY to a key from your Talos dashboard.}"
BASE_URL="${TALOS_BASE_URL:-https://api.talos.ai}"
MODEL="${TALOS_MODEL:-talos-auto}"

curl "$BASE_URL/v1/messages" \
  -H "x-api-key: $TALOS_API_KEY" \
  -H "anthropic-version: 2023-06-01" \
  -H "content-type: application/json" \
  -d "{\"model\":\"$MODEL\",\"max_tokens\":128,\"messages\":[{\"role\":\"user\",\"content\":\"Say hi\"}]}"
