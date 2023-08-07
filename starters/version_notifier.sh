#! /bin/bash

# === CONFIG ===
APP_DIR="$HOME/.apps/version_notifier/"
PYTHON_PATH="/home/siffreinsg/.pyenv/shims/"
# === END CONFIG ===

# === LOCK ===
# To be implemented...
# === END LOCK ===

# === MAIN SCRIPT ===
cd "$APP_DIR" || exit 1

"$PYTHON_PATH"/python version_notifier.py --notifier_id 2
