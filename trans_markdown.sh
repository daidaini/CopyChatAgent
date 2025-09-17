#!/bin/bash
pandoc "$1" -o "$2" \
  --standalone \
  --highlight-style=kate \
  --template='/root/CODE/Tools/pandoc_css/custom_template.html' \
  --toc \
  --toc-depth=2 \
  --metadata title="$(basename "$1" .md)"
