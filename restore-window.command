#!/usr/bin/env bash
DIR="$(cd "$(dirname "$0")" && pwd)"
"$DIR/scripts/restore-app-window.sh" --app IdleHeroTD --center
echo
read -r -p "Enter para fechar…"
