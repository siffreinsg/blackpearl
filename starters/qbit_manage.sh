#!/bin/bash

# === CONFIG ===
APP_DIR="/home/siffreinsg/.apps/qbit_manage"
CONFIG_PATH="/home/siffreinsg/.apps/qbit_manage/config/config.yaml"
PYTHON_PATH="/home/siffreinsg/.pyenv/shims/"
# === END CONFIG ===

# === LOCK ===
# To be implemented...
# === END LOCK ===

# === MAIN SCRIPT ===
cd "$APP_DIR" || exit 1

"$PYTHON_PATH"/python qbit_manage.py --config-file="$CONFIG_PATH" --run $@
