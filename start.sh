until python3 src/main.py; do
	echo "Thu'um TTS bot crashed with exit code $?. Restarting..." >&2
	sleep 1
done
