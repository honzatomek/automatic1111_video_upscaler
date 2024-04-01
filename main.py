import os
import ffmpeg
from PIL import Image
import webuiapi

def upscale_img_batch(input_frames, output_frames, width, height):
    print(f"Performing image Upscale")
    # Create API client with custom host, port
    api = webuiapi.WebUIApi(host='192.168.50.210', port=7860)

    # Open the input frames as PIL images
    pil_images = [Image.open(frame) for frame in input_frames]

    # Perform batch upscaling
    result = api.extra_batch_images(images=pil_images,
                                    upscaler_1=webuiapi.Upscaler.ESRGAN_4x,
                                    upscaling_resize_w=width, upscaling_resize_h=height)

    # Save the upscaled images
    for i, image in enumerate(result.images):
        image.save(output_frames[i])

def resize_video(input_video, output_video, output_width, output_height):
    # Create a temporary directory to store the extracted frames
    temp_dir = "temp_frames"
    if os.path.exists(temp_dir):
        for file in os.listdir(temp_dir):
            os.remove(os.path.join(temp_dir, file))
        os.rmdir(temp_dir)

    os.makedirs(temp_dir, exist_ok=True)

    # Extract frames from the video
    try:
        (
            ffmpeg
            .input(input_video)
            .output(f"{temp_dir}/frame%04d.jpg", qscale=2)
            .global_args('-y')  # Overwrite output files without asking
            .run(capture_stdout=True, capture_stderr=True)
        )
    except ffmpeg.Error as e:
        print(f"FFmpeg error: {e.stderr.decode('utf-8')}")
        return

    # Get the total number of frames
    num_frames = len(os.listdir(temp_dir))
    print(f"Number of frames: {num_frames}")

    # Prepare input and output frame paths
    input_frames = [f"{temp_dir}/frame{i:04d}.jpg" for i in range(1, num_frames + 1)]
    output_frames = [f"{temp_dir}/resized_frame{i:04d}.jpg" for i in range(1, num_frames + 1)]

    # Perform batch upscaling
    upscale_img_batch(input_frames, output_frames, output_width, output_height)

    # Stitch the resized frames back into a video
    resized_video_stream = ffmpeg.input(f"{temp_dir}/resized_frame%04d.jpg", pattern_type='sequence', framerate=30)

    # Extract audio from the original video
    audio_stream = ffmpeg.input(input_video).audio

    # Merge the resized video with the extracted audio
    try:
        (
            ffmpeg
            .output(audio_stream, resized_video_stream, output_video, vcodec='mpeg4', acodec='aac')
            .global_args('-y')  # Overwrite output files without asking
            .run(capture_stdout=True, capture_stderr=True)
        )
    except ffmpeg.Error as e:
        print(f"FFmpeg Error: {e.stderr.decode('utf-8')}")
    except Exception as e:
        print(f"General Exception: {e}")

    # Clean up temporary files and directory
    for file in os.listdir(temp_dir):
        os.remove(os.path.join(temp_dir, file))
    os.rmdir(temp_dir)

# Example usage
resize_video("bruh.mp4", "output_video.mp4", 1920, 1080)