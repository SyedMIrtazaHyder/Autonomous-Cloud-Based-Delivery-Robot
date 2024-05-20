import subprocess

## Author: Mahmood Mustafa Youssef Shilleh
## DONATE AT: https://buymeacoffee.com/mmshilleh

# YouTube Stream URL and Key
TWITCH_URL = "rtmp://live-lhr.twitch.tv/app"
TWITCH_KEY = "live_1082758854_OllSROgsacEu073wym73U0bOE0ZYtl"  # Replace with your actual YouTube stream key

# Construct the FFmpeg command for streaming


stream_cmd = f'ffmpeg -f v4l2 -framerate 25 -video_size 240x240 -i /dev/video0 -c:v libx264 -b:v 700k -maxrate 700k -bufsize 700k -an -f flv {TWITCH_URL}/{TWITCH_KEY}'

# Start the streaming subprocess
stream_pipe = subprocess.Popen(stream_cmd, shell=True, stdin=subprocess.PIPE)