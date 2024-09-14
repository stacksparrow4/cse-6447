#!/bin/bash

if [ ! -f /tmp/pwntoolscode-waiting ]; then
  echo "Tried to spawn terminal but VSCode did not have the terminal waiting."
  echo "Perhaps you forgot to run using the Play button in VSCode?"
  exit 1
fi

echo "$@" > /tmp/pwntoolscode-dbgcmd