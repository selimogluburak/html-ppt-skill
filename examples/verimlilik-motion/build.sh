#!/usr/bin/env bash
# ./build.sh → verimlilik-tanitim.mp4 (31 sn, 1920×1080, 30 fps, H.264 crf 18, yuv420p + AAC ses) ve _kontrol.jpg
# Gerekenler: Node + global playwright (Chromium), Python 3 + numpy, ffmpeg (PATH'te ya da FFMPEG=/yol/ffmpeg).
set -e
cd "$(dirname "$0")"
FF=${FFMPEG:-ffmpeg}; DUR=31; OUT=verimlilik-tanitim.mp4
rm -rf _frames; node render.mjs _frames 30 0 $DUR ${WORKERS:-2}   # kareler + sfx.json
python3 sfx.py $DUR
$FF -loglevel error -y -framerate 30 -i _frames/%05d.jpg -i sfx.wav -map 0:v -map 1:a \
  -vf "scale=in_range=pc:out_range=tv,format=yuv420p" -c:v libx264 -crf 18 -preset slow -pix_fmt yuv420p -color_range tv \
  -c:a aac -b:a 192k -ar 48000 -t $DUR -movflags +faststart $OUT
$FF -loglevel error -y -i $OUT -vf "fps=1,scale=480:-1,tile=4x8" -frames:v 1 _kontrol.jpg
rm -rf _frames sfx.wav
echo "✓ $OUT"
