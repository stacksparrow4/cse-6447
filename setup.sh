#!/bin/bash

mkdir -p .connection

echo "Please enter your ZID to connect to CSE:"
read zid

grep -qE '^z[0-9]{7}' <<< "$zid" || { echo "Invalid zid"; exit 1; }

ssh-keygen -t ed25519 -f .connection/id_cse -P ""

echo "Connecting to CSE via SSH. You will need to enter your zPass."
ssh "$zid"@cse.unsw.edu.au "mkdir -p ~/.ssh && echo '$(cat .connection/id_cse.pub)' >> ~/.ssh/authorized_keys" || { echo "Failed to register keys!"; exit 1; }
echo "Successfully registered keys."

echo "Installing pwndbg on remote..."
ssh -i .connection/id_cse "$zid"@cse.unsw.edu.au "git clone https://github.com/pwndbg/pwndbg && cd pwndbg && sed -iE 's/sudo apt-get install/#/' setup.sh && ./setup.sh" || { echo "Failed to install pwndbg on cse!"; exit 1; }
echo "Pwndbg installed!"

echo "$zid" > .connection/zid

echo "You are ready to roll! :P"
