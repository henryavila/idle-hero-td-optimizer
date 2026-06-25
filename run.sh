#!/usr/bin/env bash
set -euo pipefail

APP_DIR="$(cd "$(dirname "$0")" && pwd)"
APP_SCRIPT="ui/app.py"
APP_PORT="${IDLE_HERO_TD_PORT:-8501}"
APP_URL="http://localhost:${APP_PORT}"
PID_FILE="${APP_DIR}/tmp/streamlit.pid"

cd "$APP_DIR"

if [[ ! -d .venv ]]; then
  echo "Missing .venv. Run ./install.sh first."
  exit 1
fi

mkdir -p "$(dirname "$PID_FILE")"

find_app_pids() {
  local pid
  local cmd

  if [[ -f "$PID_FILE" ]]; then
    pid="$(cat "$PID_FILE" 2>/dev/null || true)"
    if [[ -n "$pid" ]] && kill -0 "$pid" 2>/dev/null; then
      cmd="$(ps -ww -p "$pid" -o command= 2>/dev/null || true)"
      if [[ "$cmd" == *"${APP_DIR}/.venv/bin/streamlit run ${APP_SCRIPT}"* ]]; then
        echo "$pid"
      fi
    fi
  fi

  pgrep -f "streamlit run ${APP_SCRIPT}" 2>/dev/null | while read -r pid; do
    cmd="$(ps -ww -p "$pid" -o command= 2>/dev/null || true)"
    if [[ "$cmd" == *"${APP_DIR}/.venv/bin/streamlit run ${APP_SCRIPT}"* ]]; then
      echo "$pid"
    fi
  done
}

stop_existing_app() {
  local pids
  pids="$(find_app_pids | sort -u | tr '\n' ' ')"

  if [[ -z "${pids// }" ]]; then
    return
  fi

  echo "Restarting existing Idle Hero TD Optimizer instance(s): ${pids}"
  kill $pids 2>/dev/null || true

  for _ in {1..30}; do
    local still_running=""
    for pid in $pids; do
      if kill -0 "$pid" 2>/dev/null; then
        still_running="${still_running} ${pid}"
      fi
    done
    if [[ -z "${still_running// }" ]]; then
      break
    fi
    sleep 0.2
  done

  for pid in $pids; do
    if kill -0 "$pid" 2>/dev/null; then
      kill -9 "$pid" 2>/dev/null || true
    fi
  done
}

port_pids() {
  lsof -tiTCP:"$APP_PORT" -sTCP:LISTEN 2>/dev/null || true
}

wait_for_server() {
  for _ in {1..80}; do
    if curl -fsS "$APP_URL" >/dev/null 2>&1; then
      return 0
    fi
    sleep 0.25
  done
  return 1
}

open_app() {
  if command -v open >/dev/null 2>&1; then
    open "$APP_URL"
  else
    echo "Open: $APP_URL"
  fi
}

stop_existing_app

busy_pids="$(port_pids | sort -u | tr '\n' ' ')"
if [[ -n "${busy_pids// }" ]]; then
  echo "Port ${APP_PORT} is already in use by another process: ${busy_pids}"
  echo "Close it or set IDLE_HERO_TD_PORT to another free port."
  exit 1
fi

source .venv/bin/activate
streamlit run "$APP_SCRIPT" \
  --server.address localhost \
  --server.port "$APP_PORT" \
  --server.headless true &

server_pid=$!
echo "$server_pid" > "$PID_FILE"

cleanup() {
  rm -f "$PID_FILE"
}
trap cleanup EXIT

if wait_for_server; then
  echo "Idle Hero TD Optimizer running at ${APP_URL}"
  open_app
else
  echo "Server did not start at ${APP_URL}."
  kill "$server_pid" 2>/dev/null || true
  wait "$server_pid" 2>/dev/null || true
  exit 1
fi

wait "$server_pid"
