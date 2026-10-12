#!/usr/bin/env bash
# Preview only: keys the green out of a graphics render and lays it over the face
# sample still, so you can check that the cards stay clear of the face.
#   scripts/composite.sh renders/bluehost-A-swiss-graphics.mp4 renders/bluehost-A-swiss-preview.mp4
set -euo pipefail
cd "$(dirname "$0")/.."
ffmpeg -y -loglevel error -loop 1 -framerate 30 -i reference/face-sample.webp -i "$1" \
  -filter_complex "[0:v]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,setsar=1[bg];[1:v]chromakey=0x00FF00:0.16:0.06,despill=green[fg];[bg][fg]overlay=shortest=1,format=yuv420p[v]" \
  -map "[v]" -map 1:a -c:v libx264 -crf 20 -preset medium -c:a aac -b:a 192k -shortest "$2"
echo "wrote $2"
