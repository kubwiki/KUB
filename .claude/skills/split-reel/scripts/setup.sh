#!/bin/bash
# Split-Reel - Einrichtung. Installiert alles, was fehlt (nur kostenlose Werkzeuge).
# Aufruf:  bash setup.sh            (Grundausstattung)
#          bash setup.sh --voice    (zusaetzlich: Stimmen-Trenner demucs, ca. 1 GB)
#          bash setup.sh --check    (nur pruefen, nichts installieren)
set -u
HC_HOME="${HC_HOME:-$HOME/.hollywood-cut}"
VENV="$HC_HOME/venv"
MODE="${1:-}"

say() { echo "[Split-Reel] $*"; }

if [ "$MODE" = "--check" ]; then
  for t in ffmpeg ffprobe yt-dlp; do command -v $t >/dev/null && echo "ok   $t" || echo "FEHLT $t"; done
  [ -x "$VENV/bin/python" ] && echo "ok   Python-Umgebung ($VENV)" || echo "FEHLT Python-Umgebung"
  [ -x "$VENV/bin/python" ] && "$VENV/bin/python" -c "
import importlib
for m in ['numpy','PIL','cv2','faster_whisper','scipy']:
    try: importlib.import_module(m); print('ok  ',m)
    except Exception: print('FEHLT',m)
for m in ['demucs','soundfile','torch']:
    try: importlib.import_module(m); print('ok   (Stimmentrenner)',m)
    except Exception: print('fehlt (nur noetig bei Hintergrundmusik im Video):',m)
"
  exit 0
fi

# 1) Homebrew-Programme: ffmpeg, yt-dlp
need=""
command -v ffmpeg >/dev/null || need="$need ffmpeg"
command -v yt-dlp >/dev/null || need="$need yt-dlp"
if [ -n "$need" ]; then
  if command -v brew >/dev/null; then
    say "Installiere$need ueber Homebrew ..."
    brew install $need || { say "Homebrew-Installation fehlgeschlagen:$need"; exit 1; }
  else
    say "Homebrew fehlt. Bitte einmal von https://brew.sh installieren (ein Befehl), dann Split-Reel nochmal starten."
    exit 1
  fi
fi

# 2) Python-Umgebung (eigener Ordner, beruehrt nichts anderes auf dem Rechner)
PYBIN=""
for c in python3.12 python3.11 python3.13 python3; do
  if command -v $c >/dev/null; then PYBIN=$(command -v $c); break; fi
done
[ -z "$PYBIN" ] && { say "Kein Python gefunden. 'brew install python@3.12' ausfuehren."; exit 1; }
if [ ! -x "$VENV/bin/python" ]; then
  say "Lege Python-Umgebung an in $VENV ($PYBIN) ..."
  mkdir -p "$HC_HOME"; "$PYBIN" -m venv "$VENV" || exit 1
fi
PIP="$VENV/bin/python -m pip"
$PIP install -q --upgrade pip
say "Installiere Bild- und Audio-Werkzeuge (numpy, Pillow, opencv, scipy) ..."
$PIP install -q numpy pillow "opencv-python-headless<5" scipy || exit 1
say "Installiere Spracherkennung (faster-whisper) ..."
$PIP install -q faster-whisper || exit 1

# 3) Optional: Stimmen-Trenner
if [ "$MODE" = "--voice" ]; then
  say "Installiere Stimmen-Trenner demucs (gross, dauert ein paar Minuten) ..."
  $PIP install -q "torch<2.9" "torchaudio<2.9" soundfile demucs || exit 1
fi
say "Fertig. Python: $VENV/bin/python"
