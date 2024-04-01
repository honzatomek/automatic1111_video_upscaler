from video_upscaler import VideoUpscaler

upscaler = VideoUpscaler(host='192.168.50.210', port=7860)
upscaler.upscale_video("bruh.mp4", "output_video.mp4", 1920, 1080)