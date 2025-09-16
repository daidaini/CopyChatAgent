#!/bin/bash
pandoc "$1" -o "$2" \
  --standalone \
  --highlight-style=kate \
  --template='/home/yubo/indl_dev/my_tools/pandoc_css/custom_template.html' \
  --toc \
  --toc-depth=2 \
  --metadata title="$(basename "$1" .md)"
