#!/usr/bin/env bash
# Restaura o tamanho da janela de um app no macOS.
#
# Dois casos:
#   1) App de iPhone/iPad no Mac (IdleHeroTD, Skull Hero, …)
#      Janela → Zoom devolve o tamanho de desenho. set size via
#      Accessibility não pega — a janela ignora.
#   2) App nativo do Mac
#      Zoom PREENCHE a tela. Passe --size LARGURAxALTURA.
#
# Uso:
#   restore-app-window.sh                          # IdleHeroTD + Zoom
#   restore-app-window.sh --app IdleHeroTD
#   restore-app-window.sh --app Safari --size 1280x800
#   restore-app-window.sh --app IdleHeroTD --center
#   restore-app-window.sh --app IdleHeroTD --launch
#
# Keyboard Maestro: ação Execute a Shell Script, este arquivo.

set -euo pipefail

APP="IdleHeroTD"
SIZE=""
CENTER=0
LAUNCH=0
ZOOM=""   # auto | 1 | 0

usage() {
  sed -n '2,18p' "$0" | sed 's/^# \{0,1\}//'
  exit "${1:-0}"
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    -a|--app)    APP="${2:?}"; shift 2 ;;
    -s|--size)   SIZE="${2:?}"; shift 2 ;;
    -c|--center) CENTER=1; shift ;;
    -l|--launch) LAUNCH=1; shift ;;
    -z|--zoom)   ZOOM=1; shift ;;
    --no-zoom)   ZOOM=0; shift ;;
    -h|--help)   usage 0 ;;
    *)
      echo "opção desconhecida: $1" >&2
      usage 1
      ;;
  esac
done

if [[ -z "$ZOOM" ]]; then
  if [[ -n "$SIZE" ]]; then
    ZOOM=0
  else
    ZOOM=1
  fi
fi

if [[ "$ZOOM" -eq 0 && -z "$SIZE" ]]; then
  echo "app nativo precisa de --size LARGURAxALTURA (ex.: 1280x800)" >&2
  exit 2
fi

WIDTH=""
HEIGHT=""
if [[ -n "$SIZE" ]]; then
  if [[ "$SIZE" =~ ^([0-9]+)[xX]([0-9]+)$ ]]; then
    WIDTH="${BASH_REMATCH[1]}"
    HEIGHT="${BASH_REMATCH[2]}"
  else
    echo "--size deve ser LARGURAxALTURA (ex.: 1051x820)" >&2
    exit 2
  fi
fi

# Zoom é toggle. Só dispara se a janela estiver grande demais
# (resto de tela cheia). 1051x820 do IdleHeroTD fica abaixo do limiar.
ZOOM_MIN_W="${ZOOM_MIN_W:-1200}"
ZOOM_MIN_H="${ZOOM_MIN_H:-900}"

if [[ "$LAUNCH" -eq 1 ]]; then
  if ! pgrep -qx -- "$APP" && ! pgrep -q -- "$APP"; then
    open -a "$APP" 2>/dev/null || open -a "${APP}.app" 2>/dev/null || true
    for _ in $(seq 1 40); do
      pgrep -q -- "$APP" && break
      sleep 0.25
    done
  fi
fi

if ! pgrep -q -- "$APP"; then
  echo "app não está aberto: $APP" >&2
  echo "abra o jogo ou passe --launch" >&2
  exit 3
fi

# AppleScript: menus em pt-BR e en, sem clicar no botão verde
# (Option+verde neste app virou tela cheia 2560×1080).
osascript \
  - "$APP" "$ZOOM" "$CENTER" "${WIDTH:-}" "${HEIGHT:-}" "$ZOOM_MIN_W" "$ZOOM_MIN_H" <<'APPLESCRIPT'
on run argv
  set procName to item 1 of argv
  set doZoom to (item 2 of argv is "1")
  set doCenter to (item 3 of argv is "1")
  set wantW to item 4 of argv
  set wantH to item 5 of argv
  set zoomMinW to item 6 of argv as integer
  set zoomMinH to item 7 of argv as integer

  tell application "System Events"
    if not (exists process procName) then error "processo não encontrado: " & procName
    tell process procName
      set frontmost to true
      delay 0.15
      if (count of windows) is 0 then error "nenhuma janela visível em " & procName

      set beforeTxt to my winInfo(window 1)

      my exitFullScreen(procName)
      delay 0.25

      if doZoom then
        set cur to size of window 1
        set curW to item 1 of cur
        set curH to item 2 of cur
        if curW >= zoomMinW or curH >= zoomMinH then
          my clickMenu(procName, {"Janela", "Window"}, {"Zoom"})
          delay 0.35
        end if
      end if

      if wantW is not "" and wantH is not "" then
        try
          set size of window 1 to {wantW as integer, wantH as integer}
          delay 0.2
        end try
      end if

      if doCenter then
        my clickMenu(procName, {"Janela", "Window"}, {"Centralizar", "Center"})
        delay 0.2
      end if

      set afterTxt to my winInfo(window 1)
      return beforeTxt & " -> " & afterTxt
    end tell
  end tell
end run

on winInfo(w)
  tell application "System Events"
    set s to size of w
    set p to position of w
    return ((item 1 of s) as text) & "x" & ((item 2 of s) as text) & " @ " & ((item 1 of p) as text) & "," & ((item 2 of p) as text)
  end tell
end winInfo

on exitFullScreen(procName)
  -- Só sai se o item de sair existir. Escape sozinho em jogo come input.
  try
    my clickMenu(procName, {"Visualizar", "View"}, {"Sair do Modo de Tela Cheia", "Sair de Tela Cheia", "Exit Full Screen"})
  end try
end exitFullScreen

on clickMenu(procName, barNames, itemNames)
  tell application "System Events"
    tell process procName
      tell menu bar 1
        repeat with barName in barNames
          if exists menu bar item barName then
            tell menu bar item barName
              tell menu 1
                repeat with itemName in itemNames
                  if exists menu item itemName then
                    click menu item itemName
                    return true
                  end if
                end repeat
              end tell
            end tell
          end if
        end repeat
      end tell
    end tell
  end tell
  return false
end clickMenu
APPLESCRIPT
