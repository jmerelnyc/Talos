#!/usr/bin/env bash
# Quick check: confirms your Talos key and the gateway work before wiring up
# JetBrains AI Assistant.
set -euo pipefail

: "${TALOS_API_KEY:?Set TALOS_API_KEY to a key from your Talos dashboard.}"
BASE_URL="${TALOS_BASE_URL:-https://api.usetalos.xyz/v1}"
MODEL="${TALOS_MODEL:-talos-auto}"

curl "$BASE_URL/chat/completions" \
  -H "Authorization: Bearer $TALOS_API_KEY" \
  -H "Content-Type: application/json" \
  -d "{\"model\":\"$MODEL\",\"messages\":[{\"role\":\"user\",\"content\":\"Say hi\"}]}"
