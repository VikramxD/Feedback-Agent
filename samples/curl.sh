#!/bin/bash

# RUN FILEWATCHER AND COWJ FIRST
# instead of curl you can run this file which automatically curls -T's the mp3 files in the audio folder

audio_dir="./audio"
url="http://localhost:4242/entry/u42"

# time in seconds you want to wait after each upload, persist-queue exists btw so don't feel TOO pressured.
sleep_time=10

# maximum number of files you want to upload
max_uploads=2

# just a counter variable to keep track of uploads, Obvious but don't change the value
count=0

# Recursively finds mp3 files
find "$audio_dir" -type f -name "*.mp3" | while read -r file; do
    if [ -e "$file" ]; then
        echo "Uploading $file..."
        curl -T "$file" "$url"
        echo "Uploaded $file , Now waiting..."
        
        count=$((count + 1))
        
        if [ "$count" -ge "$max_uploads" ]; then
            echo "Uploaded $max_uploads files. Now exiting..."
            exit
        fi
        
        sleep "$sleep_time"
    else
        echo "No audio files found in $audio_dir . make sure you run the download.py file first."
    fi
done
