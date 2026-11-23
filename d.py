from pytube import YouTube

# YouTube video URL
video_url = 'https://www.youtube.com/watch?v=LKVyl94v3l8'

# Create a YouTube object
yt = YouTube(video_url)

# Get the stream for 1080p resolution
stream = yt.streams.filter(res='1080p').first()

# Download the video to the specified directory
stream.download(output_path=r'E:\New folder')
