#!/bin/bash

export NTFY_APP_DIR="$HOME/.apps/ntfy"

$HOME/bin/ntfy $1 --config "$NTFY_APP_DIR/server.yml" "${@:2}"
