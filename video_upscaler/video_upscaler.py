import os
import ffmpeg
from PIL import Image
import webuiapi

class VideoUpscaler:
    def __init__(self, host='localhost', port=7860):
        self.api = webuiapi.WebUIApi(host=host, port=port)

    def get_framerate(self, input_video):
        try:
            probe = ffmpeg.probe(input_video)
            video_stream = next((stream for stream in probe['streams'] if stream['codec_type'] == 'video'), None)
            framerate = video_stream['r_frame_rate']
            return framerate
        except ffmpeg.Error as e:
            print(f"FFmpeg error: {e.stderr.decode('utf-8')}")
            return False

    def extract_frames(self, input_video, temp_dir):
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
            return False
        return True

    def upscale_img_batch(self, input_frames, output_frames, width, height):
        print(f"Performing image Upscale")

        # Open the input frames as PIL images
        pil_images = [Image.open(frame) for frame in input_frames]

        # Perform batch upscaling
        result = self.api.extra_batch_images(images=pil_images,
                                             upscaler_1=webuiapi.Upscaler.ESRGAN_4x,
                                             upscaling_resize_w=width, upscaling_resize_h=height)

        # Save the upscaled images
        for i, image in enumerate(result.images):
            image.save(output_frames[i])

    def stitch_video(self, temp_dir, output_video, framerate, audio_stream):
        upscaled_video_stream = ffmpeg.input(f"{temp_dir}/upscaled_frame%04d.jpg", pattern_type='sequence', framerate=framerate)

        try:
            (
                ffmpeg
                .output(audio_stream, upscaled_video_stream, output_video, vcodec='mpeg4', acodec='aac')
                .global_args('-y')  # Overwrite output files without asking
                .run(capture_stdout=True, capture_stderr=True)
            )
        except ffmpeg.Error as e:
            print(f"FFmpeg Error: {e.stderr.decode('utf-8')}")
        except Exception as e:
            print(f"General Exception: {e}")

    def cleanup_files(self, temp_dir):
        for file in os.listdir(temp_dir):
            os.remove(os.path.join(temp_dir, file))
        os.rmdir(temp_dir)
        

    def upscale_video(self, input_video, output_video, output_width, output_height):
        framerate = self.get_framerate(input_video)

        # Create a temporary directory to store the extracted frames
        temp_dir = "temp_frames"
        if os.path.exists(temp_dir):
            self.cleanup_files(temp_dir)
        os.makedirs(temp_dir, exist_ok=True)

        # Extract frames from the video
        if not self.extract_frames(input_video, temp_dir):
            return

        # Get the total number of frames
        num_frames = len(os.listdir(temp_dir))
        print(f"Number of frames: {num_frames}")

        # Prepare input and output frame paths
        input_frames = [f"{temp_dir}/frame{i:04d}.jpg" for i in range(1, num_frames + 1)]
        output_frames = [f"{temp_dir}/upscaled_frame{i:04d}.jpg" for i in range(1, num_frames + 1)]

        # Perform batch upscaling
        self.upscale_img_batch(input_frames, output_frames, output_width, output_height)

        # Extract audio from the original video
        audio_stream = ffmpeg.input(input_video).audio

        # Stitch the upscaled frames back into a video
        self.stitch_video(temp_dir, output_video, framerate, audio_stream)

        # Clean up temporary files and directory
        self.cleanup_files(temp_dir)