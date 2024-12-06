#!/usr/bin/zsh

name=$1
file_name=$(basename -s '.bin' "$name")


# Convert to 16kHz sample rate for further processing by the model
ffmpeg -i "$name" -ar 16000 -ac 1 -c:a pcm_s16le "data/current/audios/${file_name}.wav"

../whisper/main $WHISPER_PROC_OPT $WHISPER_THREAD_OPT -m "../whisper/models/ggml-base.bin" -f "data/current/audios/${file_name}.wav" -np > "data/current/transcripts/${file_name}.txt"

rm -rf temp

exit 0
