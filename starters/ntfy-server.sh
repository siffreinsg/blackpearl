#!/bin/bash

# === CONFIG ===
APP_DIR="$HOME/.apps/ntfy"
# === END CONFIG ===

# === LOCK ===
# To be implemented...
# === END LOCK ===

# === MAIN SCRIPT ===
cd "$APP_DIR" || (echo "Failed to change directory." && exit 1)

./ntfy $1 --config "$APP_DIR/server.yml" "${@:2}"
