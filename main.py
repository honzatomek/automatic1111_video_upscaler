from video_resizer import VideoResizer

resizer = VideoResizer(host='192.168.50.210', port=7860)
resizer.resize_video("bruh.mp4", "output_video.mp4", 1920, 1080)