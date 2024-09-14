#!/bin/bash

if [ $# -ne 1 ]; then
  echo "Usage: ./gdb.sh <binary>"
  exit 1
fi

zid="$(cat .connection/zid | tr -d '\n')"

bname="$(basename "$1")"

ssh -i .connection/id_cse "$zid"@cse.unsw.edu.au "mkdir -p comp6447-binaries"
scp -i .connection/id_cse "$1" "$zid"@cse.unsw.edu.au:~/comp6447-binaries/"$bname"
ssh -i .connection/id_cse "$zid"@cse.unsw.edu.au "chmod +x comp6447-binaries/$bname && gdb comp6447-binaries/$bname"
