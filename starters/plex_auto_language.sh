#!/bin/bash

# === CONFIG ===
PYTHON_PATH="/home/siffreinsg/.pyenv/shims"
# === END CONFIG ===

# === ENVIRONMENT ===
SCRIPT=$(realpath "$0")
SCRIPTPATH=$(dirname "$SCRIPT")

PYTHON_SCRIPT="~/scripts/Plex_auto_language/main.py"
CONFIG_PATH="$SCRIPTPATH/../Plex_auto_language/config.yaml"

set -o allexport
source "$SCRIPTPATH/../.env"
set +o allexport
# === END ENVIRONMENT ===

# === LOCK ===
# To be implemented...
# === END LOCK ===

# === MAIN SCRIPT ===
"$PYTHON_PATH"/python "$PYTHON_SCRIPT" -c "$CONFIG_PATH" "$@"
