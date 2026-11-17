#!/bin/bash
# Split-Reel - Stimme von Hintergrundmusik trennen (demucs, lokal, kostenlos).
# Noetig, wenn das Quellvideo selbst schon Musik hat: sonst laufen zwei Musikstuecke uebereinander.
#
#   isolate_voice.sh video.mp4 stimme.wav [START ENDE]
#
# Mit START/ENDE (Sekunden im Original) wird nur dieser Teil getrennt (viel schneller).
# Die Ausgabedatei hat trotzdem die ZEITACHSE DES ORIGINALS (davor Stille) -
# sie kann in der Spezifikation direkt als "voice_src" eingetragen werden.
set -e
IN="$1"; OUT="$2"; START="${3:-0}"; END="${4:-}"
[ -z "$IN" ] || [ -z "$OUT" ] && { sed -n '2,10p' "$0"; exit 1; }
HC_HOME="${HC_HOME:-$HOME/.hollywood-cut}"
PY="$HC_HOME/venv/bin/python"
"$PY" -c "import demucs, soundfile" 2>/dev/null || { echo "Stimmen-Trenner fehlt. Zuerst: bash $(dirname "$0")/setup.sh --voice"; exit 1; }
TMP=$(mktemp -d "${TMPDIR:-/tmp}/hc_voice.XXXXXX")
if [ -n "$END" ]; then DUR=$(python3 -c "print($END-$START)"); T="-t $DUR"; else T=""; fi
ffmpeg -y -v error -ss "$START" $T -i "$IN" -vn -ac 2 -ar 44100 "$TMP/in.wav"
echo "[Split-Reel] Trenne Stimme von Musik (kann einige Minuten dauern) ..."
"$PY" -m demucs --two-stems=vocals -n htdemucs --device cpu -o "$TMP/sep" "$TMP/in.wav" >/dev/null
V=$(find "$TMP/sep" -name vocals.wav | head -1)
[ -z "$V" ] && { echo "Trennung fehlgeschlagen."; exit 1; }
MS=$(python3 -c "print(int(float($START)*1000))")
if [ "$MS" -gt 0 ]; then
  ffmpeg -y -v error -i "$V" -af "adelay=${MS}|${MS}" -ac 1 -ar 44100 "$OUT"
else
  ffmpeg -y -v error -i "$V" -ac 1 -ar 44100 "$OUT"
fi
rm -rf "$TMP"
echo "[Split-Reel] Fertig: $OUT"
