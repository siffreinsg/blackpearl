#! /bin/bash

# === CONFIG ===
APP_DIR="$HOME/.apps/version-notifier"
PYTHON_PATH="/home/siffreinsg/.pyenv/shims"
# === END CONFIG ===

# === ENVIRONMENT ===
SCRIPT=$(realpath "$0")
SCRIPTPATH=$(dirname "$SCRIPT")

PYTHON_SCRIPT="$SCRIPTPATH/../python/version_notifier.py"
# === END ENVIRONMENT ===

# === LOCK ===
# To be implemented...
# === END LOCK ===

# === MAIN SCRIPT ===
cd "$APP_DIR" || exit 1

"$PYTHON_PATH"/python "$PYTHON_SCRIPT" --notifier_id 2
