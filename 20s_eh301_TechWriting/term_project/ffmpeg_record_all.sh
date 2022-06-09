#!/bin/bash
path=$1

ffmpeg -f x11grab -s 1366x768 -i :0.0 -f alsa -i default $path

ffmpeg -i video.mp4 -i audio.wav -c:v copy -c:a aac -map 0:v:0 -map 1:a:0 output.mp4

# start cut at first time, cut is the duration of second time
# ffmpeg -ss HH:MM:SS.D -i input.mp4 -c copy -t HH:MM:SS.D output.mp4
# 18s

# combine audio-less video with audio
# ffmpeg -i video.mp4 -i audio.wav -c:v copy -c:a aac output.mp4

# replace audio in video containing audio
# ffmpeg -i video.mp4 -i audio.wav -c:v copy -c:a aac -map 0:v:0 -map 1:a:0 output.mp4
