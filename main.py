#!/home/honza/Programming/stable-diffusion-video-upscaler/__venv__/bin/python3.10
"""Video Upscaler using Stable-Diffusion WebUI"""

import os
import sys
import re
import argparse
import subprocess


ROOT = os.path.dirname(os.path.realpath(__file__))
if ROOT not in sys.path:
    sys.path.append(ROOT)

from video_upscaler import VideoUpscaler


def video_orig_size(filename: str) -> (int, int):
    filename = os.path.realpath(filename)

    ffprobe = subprocess.check_output(["ffprobe", filename], stderr=subprocess.STDOUT).decode()

    for line in ffprobe.split("\n"):
        m = re.match(r"^\s*Stream\s+#.*?Video:.*?\s(?P<size>\d+[x]\d+),.*$", line, re.I)
        if m:
            size = m["size"].split("x")
            return int(size[0]), int(size[1])
    else:
        return None, None



if __name__ == "__main__":
    # Create options parser object.
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawTextHelpFormatter)

    # Add arguments
    parser.add_argument("--ip", dest="ip", type=str, default="localhost",
                        help="IP address of the running Stable Diffusion WebUI (default = localhost).")

    parser.add_argument("--port", dest="port", type=int, default=7860,
                        help="The port of the running Stable Diffusion WebUI (default = 7860).")

    parser.add_argument("-s", "--scale", type=float, default=2.0,
                        help="The scale of the output picture (default = 3).")

    parser.add_argument("--size", nargs=2, type=float, default=None,
                        help="The width and height of the output video in px, overrides scale (defalut = None).")

    parser.add_argument("input_video", type=str, help="Path to the video to upscale.")

    # Parse command-line arguments.
    args = parser.parse_args()

    args.input_video = os.path.realpath(args.input_video)

    if args.size is None:
        input_width, input_height = video_orig_size(args.input_video)
        if input_width is None:
            raise IOError(f"Cannot specify {args.input_video:s} original size, the new size must be set manually.")
        output_width = int(float(args.scale) * input_width)
        output_height = int(float(args.scale) * input_height)
    else:
        output_width = int(args.size[0])
        output_height = int(args.size[1])

    upscaler = VideoUpscaler(host=str(args.ip), port=int(args.port))

    basename, ext = os.path.splitext(args.input_video)
    output_video = f"{basename:s}_{output_width:d}x{output_height:d}{ext:s}"

    upscaler.upscale_video(args.input_video, output_video,
                           output_width, output_height, batch_limit=10)

