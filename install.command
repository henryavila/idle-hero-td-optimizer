#!/usr/bin/env bash
DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$DIR"
./install.sh
read -r -p "Press Enter to close..."
