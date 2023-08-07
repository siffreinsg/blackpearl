#!/bin/bash

# === CONFIG ===
APP_DIR="$HOME/.apps/ntfy"
# === END CONFIG ===

# === LOCK ===
# To be implemented...
# === END LOCK ===

# === MAIN SCRIPT ===
cd "$APP_DIR" || exit 1

./ntfy $1 --config "$APP_DIR/server.yml" "${@:2}"
