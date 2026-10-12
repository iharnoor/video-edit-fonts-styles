#!/usr/bin/env bash
# Pull the real Ryzen AI Halo assets from amd.com (needs www.amd.com allowed; amd.com rejects curl's default UA).
# Output: assets/amd-page/img/* (product layers, reveal video), assets/banner_frames/*.jpg, assets/amd-page/spec_crop.png
set -euo pipefail
P="$(cd "$(dirname "$0")/.." && pwd)"; D="$P/assets/amd-page/img"; mkdir -p "$D" "$P/assets/banner_frames"
UA="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130 Safari/537.36"
B=https://www.amd.com/content/dam/amd/en/images
for u in products/agent-computers/5487300-ryzen-ai-halo.png products/agent-computers/5487300-ryzen-ai-halo-{1,2,3,4,5}.png \
         backgrounds/video/4174450-product-banner.mp4; do
  curl -sS -m 120 -A "$UA" -H "Accept: image/png,video/mp4,*/*;q=0.5" -o "$D/$(basename "$u" | sed 's/^4174450-//')" "$B/$u"
done
# reveal video: crop around the box (1240x400) -> 480 frames
ffmpeg -v error -y -i "$D/product-banner.mp4" -vf "crop=1240:400:1040:0" -q:v 2 "$P/assets/banner_frames/f%03d.jpg"
# full-page mobile screenshot with the Max+ 395 spec tab selected, then crop the 128GB / 200B tiles
NODE_PATH="$(npm root -g)" node "$P/scripts/capture_amd_page.js" "$P/assets/amd-page"
python3 -c "
from PIL import Image; Image.MAX_IMAGE_PIXELS=None
Image.open('$P/assets/amd-page/full395.png').crop((0,int(2365*2.5),1080,int(2600*2.5))).save('$P/assets/amd-page/spec_crop.png')"
