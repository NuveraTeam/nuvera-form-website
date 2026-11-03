#!/bin/sh
# Rebuilds assets/tw.css from the Tailwind classes used in index.html.
# Run after changing classes in index.html. Needs the Tailwind v3 standalone CLI:
#   https://github.com/tailwindlabs/tailwindcss/releases/tag/v3.4.17
set -e
cd "$(dirname "$0")/.."
printf '@tailwind base;\n@tailwind components;\n@tailwind utilities;\n' > /tmp/nf-tw-in.css
printf 'module.exports={content:["./index.html"],theme:{extend:{}},plugins:[]}\n' > /tmp/nf-tw.config.js
${TAILWIND:-tailwindcss} -c /tmp/nf-tw.config.js -i /tmp/nf-tw-in.css -o assets/tw.css --minify
