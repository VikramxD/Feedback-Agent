# Run all of this to download 200-ish audio mp3 files, do it inside the samples directory

# pip3 install pytubefix first

import os
from pytubefix import Playlist

url = "https://www.youtube.com/playlist?list=PLUV23VNSuzGHNJ7ccWKQPtaS4fGBTTcyL"  # Can add any youtube playlist audio
# It's downloading 1 minute perfume reviews for now

pl = Playlist(url) # https://github.com/JuanBindez/pytubefix
os.makedirs('audio', exist_ok=True) 

for video in pl.videos: 
    ys = video.streams.get_audio_only()
    title = video.title
    strip_title = "".join(c for c in title if c.isalnum() or c in "._- ")
    output_path = os.path.join('audio', f"{strip_title}.mp3")
    ys.download(output_path=output_path, mp3=True)
    print(f"Downloaded: {output_path}")