#!/bin/bash

export DOTNET_GCHeapHardLimit=10000000
export RECYCLARR_APP_DATA="$HOME/.apps/recyclarr/"

$HOME/bin/recyclarr.real "$@"
