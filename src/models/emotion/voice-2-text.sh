#!/usr/bin/zsh
###################
# https://github.com/ggerganov/whisper.cpp
# This is done for SQS
##################
# home for whisper installation
#WHISPER_HOME="/home/journaly/whisper"
#/home/ajafri/Desktop/whisper.cpp/main
# input file to process
IN_FILE=$1
# working directory to be used temporarily
WORKING_DIR=$2
# copy from s3 to local for faster processing
cp "$IN_FILE" "$WORKING_DIR/"
# get the name of the file removing directory and extension
file_name=$(basename -s '.bin' "$IN_FILE")
# run the ffmpeg to create wav file
ffmpeg -i "$WORKING_DIR/$file_name.bin" -ar 16000 -ac 1 -c:a pcm_s16le "$WORKING_DIR/$file_name.wav"


# TODO; Need to further preprocess the data to make it suitable for the v.e model [trimming off trailing ends etc]

###############################
# Processors and Thread options for Whisper 
# -p 4 --> 4 processors ( default 1 )
# -t 4 --> 4 threads ( default )
# Pick option by running the stewy.wav with various combo
# Which runs with lowest time in sec
# On noga's HONOR AMD Ryzen, -p 4 with default threads run fastest ~ 8 sec
###############################
WHISPER_PROC_OPT=""
WHISPER_THREAD_OPT=""

#############################################################################
# Model is picked with multi-lingual base - many languages supported
# Options are: https://github.com/ggerganov/whisper.cpp/blob/master/models/README.md#available-models 
# ggml-base ggml-small ggml-medium ggml-large
# We found out base works for most, for some borderline cases small to medium 
##############################################################################

# run whisper to transcribe the stuff
# $WHISPER_HOME/main  $WHISPER_PROC_OPT $WHISPER_THREAD_OPT -m "$WHISPER_HOME/models/ggml-base.bin" -f "$WORKING_DIR/$file_name.wav"  -np > "$WORKING_DIR/$file_name.txt"


# ADDED RELATIVE FILE PATHS INSTEAAD SINCE WHISPER IS NOW SELF CONTAINED
../whisper/main $WHISPER_PROC_OPT $WHISPER_THREAD_OPT -m "../whisper/models/ggml-base.bin" -f "$WORKING_DIR/${file_name}.wav" -np > "$WORKING_DIR/${file_name}.txt"


# remove the original file from here
rm "$WORKING_DIR/$file_name.bin"
# exit with 0, all good
exit 0
