# Video Resizer

Video Resizer is a Python package that allows you to resize videos using the Automatic1111 web UI. It provides a convenient way to upscale video resolution while maintaining the original framerate and audio.

## Features

- Resize videos to a specified width and height
- Maintain the original framerate of the video
- Preserve the audio from the original video
- Utilize the Automatic1111 web UI for high-quality upscaling

## Requirements

- Python 3.6 or higher
- FFmpeg installed and available in the system PATH
- Automatic1111 web UI running with the `--api` flag

## Installation

1. Make sure you have FFmpeg installed on your system. You can download it from the official website: [https://ffmpeg.org/](https://ffmpeg.org/)

2. Set up the Automatic1111 web UI:
   - Clone the repository: [https://github.com/AUTOMATIC1111/stable-diffusion-webui](https://github.com/AUTOMATIC1111/stable-diffusion-webui)
   - Follow the installation instructions provided in the repository's README.
   - Launch the web UI with the `--api` flag to enable the API access:
     ```
     python launch.py --api
     ```

3. Install the Video Resizer package using pip:
   ```
   pip install video-resizer
   ```

## Usage

1. Import the `VideoResizer` class from the package:
   ```python
   from video_resizer import VideoResizer
   ```

2. Create an instance of the `VideoResizer` class:
   ```python
   resizer = VideoResizer(host='localhost', port=7860)
   ```
   - `host`: The hostname or IP address where the Automatic1111 web UI is running (default: `'localhost'`).
   - `port`: The port number on which the Automatic1111 web UI is running (default: `7860`).

3. Use the `resize_video` method to resize a video:
   ```python
   resizer.resize_video(input_video, output_video, output_width, output_height)
   ```
   - `input_video`: The path to the input video file.
   - `output_video`: The path where the resized video will be saved.
   - `output_width`: The desired width of the resized video.
   - `output_height`: The desired height of the resized video.

   Example:
   ```python
   resizer.resize_video("input_video.mp4", "output_video.mp4", 1920, 1080)
   ```

4. The resized video will be saved to the specified output path.

## Example

```python
from video_resizer import VideoResizer

# Create an instance of VideoResizer
resizer = VideoResizer(host='localhost', port=7860)

# Resize a video
resizer.resize_video("input_video.mp4", "output_video.mp4", 1920, 1080)
```

## Contributing

Contributions are welcome! If you find any issues or have suggestions for improvements, please open an issue or submit a pull request on the GitHub repository.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more information.

## Acknowledgments

- [Automatic1111 web UI](https://github.com/AUTOMATIC1111/stable-diffusion-webui) for providing the upscaling functionality.
- [FFmpeg](https://ffmpeg.org/) for video processing capabilities.

## Contact

For any questions or inquiries, please contact [your-email@example.com](mailto:your-email@example.com).