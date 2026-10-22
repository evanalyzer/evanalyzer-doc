#!/bin/sh
# One-time setup for take.py on Debian/Ubuntu: the virtual display, the
# tools that click and capture, numpy/tifffile for the demo images - and,
# when the system's glibc is older than the one EVAnalyzer is built against,
# a newer glibc in .cache/screenshots/glibc (the system's stays untouched).
set -e
ROOT=$(cd "$(dirname "$0")/../.." && pwd)
CACHE="$ROOT/.cache/screenshots"

sudo apt-get install -y xvfb xdotool imagemagick python3-numpy python3-tifffile \
  libxkbcommon-x11-0 libxcursor1 libxrandr2 libxi6 libgl1 libegl1 libfontconfig1

# The demo data goes to /data/ev_plate (a short path that reads well in the
# screenshots). Another place: export EVA_DATA=... before take.py.
if [ ! -w /data ] 2>/dev/null; then
  sudo mkdir -p /data && sudo chown "$(id -u):$(id -g)" /data
fi

APP=${EVA_APP:-$ROOT/tools/evanalyzer-linux-x86_64/evanalyzer}
if "$APP" --version >/dev/null 2>&1; then
  echo "EVAnalyzer runs with the system's libraries."
  exit 0
fi
echo "EVAnalyzer needs a newer glibc - fetching Debian trixie's into $CACHE/glibc"
mkdir -p "$CACHE/debs" "$CACHE/glibc"
cd "$CACHE/debs"
for p in libc6 libstdc++6 libgcc-s1; do
  url=$(curl -s "https://packages.debian.org/trixie/amd64/$p/download" |
    grep -o 'http://ftp.de.debian.org/debian/pool/[^"]*\.deb' | head -1)
  curl -sLO "$url"
done
for d in *.deb; do dpkg-deb -x "$d" "$CACHE/glibc"; done
LIB="$CACHE/glibc/usr/lib/x86_64-linux-gnu"
"$LIB/ld-linux-x86-64.so.2" --library-path "$LIB:/lib/x86_64-linux-gnu:/usr/lib/x86_64-linux-gnu" "$APP" --version
