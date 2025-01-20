import os
import math
import ffmpeg
from PIL import Image
import webuiapi
from tqdm import tqdm


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


    def upscale_img_batch(self, input_frames, output_frames, scale=2.0, batch_limit=100):
        print(f"Performing image frames Upscale in batches of {batch_limit:d}")

        if batch_limit is None:
            batch_limit = len(input_frames)

        # Split all images into batches
        for i in tqdm(range(0, len(input_frames), batch_limit)):
            input_batch = input_frames[i:i+batch_limit]
            output_batch = output_frames[i:i+batch_limit]

            # Open the input frames as PIL images
            pil_images = [Image.open(frame) for frame in input_batch]

            # Select upscaler
            # upscaler = webuiapi.Upscaler("R-ESRGAN 4x+")
            upscaler = webuiapi.Upscaler.ESRGAN_4x

            # Perform batch upscaling
            result = self.api.extra_batch_images(images=pil_images,
                                                 upscaler_1=upscaler,
                                                 upscaling_resize=scale)
                                                 # upscaling_resize_w=width,
                                                 # upscaling_resize_h=height)

            # Save the upscaled images
            for j, image in enumerate(result.images):
                image.save(output_batch[j])

            # close the images
            [frame.close() for frame in pil_images]

            # close the images
            [frame.close() for frame in result.images]


    def upscale_img_sequential(self, input_frames, output_frames, scale=2.):
        print(f"Performing sequential image Upscale")

        # Select upscaler
        # upscaler = webuiapi.Upscaler("R-ESRGAN 4x+")
        upscaler = webuiapi.Upscaler.ESRGAN_4x

        # Open the input frames as PIL images
        for i in tqdm(range(len(input_frames))):
            input_frame = intput_frames[i]
            output_frame = output_frames[i]
            with Image.open(input_frame) as pil_image:
                # Perform upscaling
                result = self.api.extra_single_image(image=pil_image,
                                                     upscaler_1=upscaler,
                                                     upscaling_resize=scale)

                # Save the upscaled image
                result.image.save(output_frame)


    def stitch_video(self, temp_dir, output_video, framerate, audio_stream):
        upscaled_video_stream = ffmpeg.input(f"{temp_dir}/upscaled_frame%04d.jpg", pattern_type='sequence', framerate=framerate)

        try:
            (
                ffmpeg
                .output(audio_stream, upscaled_video_stream, output_video, vcodec='h264', acodec='aac')
                .global_args('-y')  # Overwrite output files without asking
                .run(capture_stdout=True, capture_stderr=True)
            )
                #.output(audio_stream, upscaled_video_stream, output_video, vcodec='mpeg4', acodec='aac')
        except ffmpeg.Error as e:
            print(f"FFmpeg Error: {e.stderr.decode('utf-8')}")
        except Exception as e:
            print(f"General Exception: {e}")


    def cleanup_files(self, temp_dir):
        for file in os.listdir(temp_dir):
            os.remove(os.path.join(temp_dir, file))
        os.rmdir(temp_dir)


    def upscale_video(self, input_video, output_video, scale=2.0, batch_limit=100):
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
        try:
            self.upscale_img_batch(input_frames, output_frames, scale, batch_limit)
        except OSError as e:
            self.upscale_img_sequential(input_frames, output_frames, scale)

        # Extract audio from the original video
        audio_stream = ffmpeg.input(input_video).audio

        # Stitch the upscaled frames back into a video
        self.stitch_video(temp_dir, output_video, framerate, audio_stream)

        # Clean up temporary files and directory
        self.cleanup_files(temp_dir)


