#!/bin/bash

# === CONFIG ===
APP_DATA="$HOME/.apps/recyclarr/"
# === END CONFIG ===

# === LOCK ===
# To be implemented...
# === END LOCK ===

# === MAIN SCRIPT ===
echo "Updating Recyclarr..."

mkdir -p "$APP_DATA" || (echo "Failed to create directory." && exit 1)
cd "$APP_DATA" || exit 1

# Delete the old version
rm -f recyclarr || echo "No old version found, skipping."

# Fetch the latest version
echo "Fetching latest version..."
wget -q https://github.com/recyclarr/recyclarr/releases/latest/download/recyclarr-linux-x64.tar.xz || (echo "Failed to fetch latest version." && exit 1)
echo "Downloaded latest version."

# Extract and delete the archive
echo "Extracting..."
tar -xf recyclarr-linux-x64.tar.xz || (echo "Failed to extract archive." && exit 1)
rm recyclarr-linux-x64.tar.xz || (echo "Failed to delete archive." && exit 1)
echo "Extracted and deleted archive."

# Make the binary executable
echo "Making binary executable..."
chmod +x recyclarr || (echo "Failed to make binary executable." && exit 1)
echo "Binary now executable."

echo "Update complete."
