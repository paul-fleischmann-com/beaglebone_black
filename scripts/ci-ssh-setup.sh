#!/bin/sh
# Set up SSH key from SSH_KEY environment variable.
mkdir -p ~/.ssh
printf '%s\n' "$SSH_KEY" > ~/.ssh/id_rsa
chmod 600 ~/.ssh/id_rsa
