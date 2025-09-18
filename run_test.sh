#!/usr/bin/env bash
set -euo pipefail

MODE=${1:-remote}
REMOTE_URL="https://petstore3.swagger.io/api/v3"
LOCAL_URL="http://local-server:8080/api/v3"

if [[ "$MODE" == "local" ]]; then
  echo ">>> Running tests against LOCAL server..."

  PET_BASE_URL=$LOCAL_URL \
  docker compose --profile local --profile tests up --build --abort-on-container-exit

  echo ">>> Cleaning up..."
  docker compose down --volumes

elif [[ "$MODE" == "remote" ]]; then
  echo ">>> Running tests against REMOTE server: $REMOTE_URL"
  PET_BASE_URL=$REMOTE_URL \
  docker compose --profile tests run --rm tests

  echo ">>> Done. No local server was started."
else
  echo "Usage: $0 [local|remote]"
  exit 1
fi
