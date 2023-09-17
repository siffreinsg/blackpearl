#!/bin/bash

# === CONFIG ===
APP_DIR="/home/siffreinsg/.apps/joal"

export JAVA_TOOL_OPTIONS="-Xms64m -Xmx256m -XX:CompressedClassSpaceSize=256m -XX:MaxMetaspaceSize=256m -XX:MaxRAM=512m -XX:MaxRAMPercentage=70 -XX:ActiveProcessorCount=1"
# === END CONFIG ===

# === ENVIRONMENT ===
SCRIPT=$(realpath "$0")
SCRIPTPATH=$(dirname "$SCRIPT")

set -o allexport
source "$SCRIPTPATH/../.env"
set +o allexport
# === END ENVIRONMENT ===

# === LOCK ===
# To be implemented...
# === END LOCK ===

# === MAIN SCRIPT ===
cd "$APP_DIR" || exit 1

/usr/bin/java -jar "$APP_DIR/joal.jar" --joal-conf="$APP_DIR" \
    --spring.main.web-environment=true \
    --server.port=$JOAL_PORT \
    --joal.ui.path.prefix="$JOAL_PREFIX" \
    --joal.ui.secret-token="$JOAL_SECRET"
