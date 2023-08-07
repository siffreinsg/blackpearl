#!/bin/bash

# === CONFIG ===
APP_DATA="$HOME/.apps/joal/"
# === END CONFIG ===

# === LOCK ===
# To be implemented...
# === END LOCK ===

# === MAIN SCRIPT ===
echo "Updating JOAL..."

mkdir -p "$APP_DATA" || (echo "Failed to create directory." && exit 1)
cd "$APP_DATA" || (echo "Failed to change directory." && exit 1)

# Delete the old version
rm -f joal.jar || echo "No old version found, skipping."

# Fetch the latest version
echo "Fetching latest version..."
wget -q https://github.com/anthonyraymond/joal/releases/latest/download/joal.tar.gz || (echo "Failed to fetch latest version." && exit 1)
echo "Downloaded latest version."

# Extract and delete the archive
echo "Extracting..."
tar -xf joal.tar.gz || (echo "Failed to extract archive." && exit 1)
rm joal.tar.gz || (echo "Failed to delete archive." && exit 1)
echo "Extracted and deleted archive."

# Rename the jar file
echo "Renaming jar file..."
mv *.jar joal.jar || (echo "Failed to rename jar file." && exit 1)
echo "Renamed jar file."

echo "Update complete."
