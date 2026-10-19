#!/bin/sh
# usage: ./render.sh page.svg  -> page.png (850x1100)
set -e
out="${1%.svg}.png"
/opt/pw-browsers/chromium-1194/chrome-linux/chrome --headless --no-sandbox --disable-gpu \
  --screenshot="$out" --window-size=850,1300 --hide-scrollbars "file://$(pwd)/$1" 2>/dev/null
convert "$out" -crop 850x1100+0+0 +repage "$out"
