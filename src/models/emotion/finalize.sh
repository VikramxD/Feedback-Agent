#!/usr/bin/zsh
# This finalizes the stuff
# working directory to be used temporarily
WORKING_DIR=$1
#  directory to be used to copy back all files - this is MountPoint destination in S3
DESTINATION_DIR=$2
# create a folder structure first - inside MountPoint system
mkdir -p "$DESTINATION_DIR"

# copy  local files back to s3 now
# https://stackoverflow.com/questions/34254164/getting-an-error-cp-cannot-stat-when-trying-to-copy-files-from-one-folder-to-an 
#
cp "$WORKING_DIR/"*.txt  "$DESTINATION_DIR/"
cp "$WORKING_DIR/"*.json "$DESTINATION_DIR/"

# now cleans up /tmp to ensure no extra stuff
rm -rf "$WORKING_DIR"
# clean exit
exit 0
