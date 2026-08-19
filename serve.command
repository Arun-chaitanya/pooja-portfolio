#!/bin/bash
# Double-click this file (or run ./serve.command) to preview the site locally.
# YouTube embeds only play over http://, not when index.html is opened as a file.
cd "$(dirname "$0")"
PORT=8000
( sleep 1; open "http://localhost:$PORT/" ) &
echo "Serving at http://localhost:$PORT  — press Ctrl+C to stop"
python3 -m http.server $PORT
