#!/bin/bash

while true; do
    python3 src/main.py
    EXIT_CODE=$?

    # Restart if exit code is not 0 (normal termination) or 130 (KeyboardInterrupt)
    if [ $EXIT_CODE -eq 0 ] || [ $EXIT_CODE -eq 130 ]; then
        echo "Stopping with exit code $EXIT_CODE."
        break
    else
        echo "Thu'um TTS bot crashed with exit code $EXIT_CODE. Restarting..." >&2
        sleep 1
    fi
done
