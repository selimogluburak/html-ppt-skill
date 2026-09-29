#!/usr/bin/env bash
# ./build.sh [kaynak.html] → verimlilik-tanitim.mp4 (40 sn, 1920×1080, 30 fps, H.264 + AAC) ve _kontrol.jpg
# Kaynak HTML verilirse önce ui/ görüntüleri yeniden yakalanır.
# Gerekenler: Node + global playwright (Chromium), Python 3 + numpy + scipy, ffmpeg (PATH'te ya da FFMPEG=/yol/ffmpeg).
set -e
cd "$(dirname "$0")"
FF=${FFMPEG:-ffmpeg}; OUT=verimlilik-tanitim.mp4
[ -n "$1" ] && node capture.mjs "$1"
rm -rf _frames; node render.mjs _frames 30 0 "" ${WORKERS:-4}      # kareler + sfx.json
python3 sfx.py
$FF -loglevel error -y -framerate 30 -i _frames/%05d.jpg -i sfx.wav -map 0:v -map 1:a \
  -vf "format=yuv420p" -c:v libx264 -crf 20 -preset slow -tune film -pix_fmt yuv420p \
  -c:a aac -b:a 256k -ar 48000 -shortest -movflags +faststart $OUT
$FF -loglevel error -y -i $OUT -vf "fps=1,scale=480:-1,tile=5x8" -frames:v 1 _kontrol.jpg
rm -rf _frames sfx.wav sfx.json
echo "✓ $OUT"
