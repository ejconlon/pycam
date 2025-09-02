#!/usr/bin/env bash

set -euxo pipefail

if [[ "$OSTYPE" == "darwin"* ]]; then
  brew install pango cairo gdk-pixbuf gobject-introspection pygobject3
  # brew link --overwrite pango
  # brew link --overwrite cairo
  # brew link --overwrite gdk-pixbuf
fi

rm -rf .venv
python3 -m venv .venv --system-site-packages
.venv/bin/pip install -r requirements.txt
.venv/bin/pip install -e .
