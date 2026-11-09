#!/bin/bash
# Split-Reel - YouTube-Link (oder anderer Link) als MP4 herunterladen.
#   download.sh "https://youtube.com/watch?v=..." ziel_ordner
# Hinweis: Ohne den web_embedded-Client bricht YouTube oft mit 403 ab.
URL="$1"; DIR="${2:-.}"
[ -z "$URL" ] && { sed -n '2,4p' "$0"; exit 1; }
mkdir -p "$DIR"
yt-dlp --extractor-args "youtube:player_client=web_embedded,default" \
  -f "bv*[height<=1080][ext=mp4]+ba[ext=m4a]/b[height<=1080]/b" --merge-output-format mp4 \
  -o "$DIR/%(title).80s.%(ext)s" "$URL"
