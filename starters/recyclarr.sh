#!/bin/bash

# === CONFIG ===
DOTNET_GCHeapHardLimit=10000000
export RECYCLARR_APP_DATA="$HOME/.apps/recyclarr/"
# === END CONFIG ===

# === LOCK ===
# To be implemented...
# === END LOCK ===

# === MAIN SCRIPT ===
cd "$RECYCLARR_APP_DATA" || exit 1

./recyclarr "$@"
