#!/usr/bin/env bash
set -euo pipefail

APP_DIR="$(cd "$(dirname "$0")" && pwd)"
APP_SCRIPT="ui/app.py"
APP_PYTHON=".venv/bin/python"
APP_PORT="${IDLE_HERO_TD_PORT:-8501}"
APP_URL="http://localhost:${APP_PORT}"
PID_FILE="${APP_DIR}/tmp/streamlit.pid"

cd "$APP_DIR"

if [[ ! -d .venv ]]; then
  echo "Missing .venv. Run ./install.sh first."
  exit 1
fi

if [[ ! -x "$APP_PYTHON" ]]; then
  echo "Missing ${APP_PYTHON}. Run ./install.sh first."
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
      if [[ "$cmd" == *"${APP_PYTHON} -m streamlit run ${APP_SCRIPT}"* ]] || [[ "$cmd" == *"${APP_DIR}/${APP_PYTHON} -m streamlit run ${APP_SCRIPT}"* ]]; then
        echo "$pid"
      fi
    fi
  fi

  pgrep -f "streamlit run ${APP_SCRIPT}" 2>/dev/null | while read -r pid; do
    cmd="$(ps -ww -p "$pid" -o command= 2>/dev/null || true)"
    if [[ "$cmd" == *"${APP_PYTHON} -m streamlit run ${APP_SCRIPT}"* ]] || [[ "$cmd" == *"${APP_DIR}/${APP_PYTHON} -m streamlit run ${APP_SCRIPT}"* ]]; then
      echo "$pid"
    fi
  done || true
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

confirm_and_stop_busy_port() {
  local pids="$1"
  local answer=""
  local still_busy=""

  echo "Porta ${APP_PORT} ja esta em uso pelo(s) processo(s): ${pids}"
  printf "Fechar esse(s) processo(s) e continuar? [s/N] "
  if ! read -r answer; then
    echo
    answer=""
  fi

  case "$answer" in
    s|S|sim|SIM|Sim|y|Y|yes|YES|Yes)
      ;;
    *)
      echo "Mantendo processo(s). Feche-os ou defina IDLE_HERO_TD_PORT para outra porta livre."
      return 1
      ;;
  esac

  kill $pids 2>/dev/null || true

  for _ in {1..30}; do
    still_busy="$(port_pids | sort -u | tr '\n' ' ')"
    if [[ -z "${still_busy// }" ]]; then
      return 0
    fi
    sleep 0.2
  done

  echo "Porta ${APP_PORT} continua em uso pelo(s) processo(s): ${still_busy}"
  echo "Nao foi possivel resolver automaticamente."
  return 1
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
  confirm_and_stop_busy_port "$busy_pids"
fi

"$APP_PYTHON" -m streamlit run "$APP_SCRIPT" \
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
