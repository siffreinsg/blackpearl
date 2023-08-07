#!/bin/bash

# === CONFIG ===
APP_DATA="$HOME/.config/qBittorrent/VueTorrent/"
# === END CONFIG ===

# === LOCK ===
# To be implemented...
# === END LOCK ===

# === MAIN SCRIPT ===
echo "Updating VueTorrent..."

mkdir -p "$APP_DATA" || (echo "Failed to create directory." && exit 1)
cd "$APP_DATA" || (echo "Failed to change directory." && exit 1)

# Pull the latest version
echo "Pulling latest version..."
git pull || (echo "Failed to pull latest version." && exit 1)
echo "Pulled latest version."

echo "Update complete."
