#!/bin/bash

APP_PATH="/home/siffreinsg/.apps/qbit_manage"
CONFIG_PATH="/home/siffreinsg/.apps/qbit_manage/config/config.yaml"
PYTHON_PATH="/home/siffreinsg/.pyenv/shims/"

cd "$APP_PATH"

"$PYTHON_PATH"/python qbit_manage.py --config-file="$CONFIG_PATH" $@
