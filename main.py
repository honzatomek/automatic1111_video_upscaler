#!/home/honza/Programming/stable-diffusion-video-upscaler/__venv__/bin/python3.10
"""Video Upscaler using Stable-Diffusion WebUI"""

import os
import sys
import re
import argparse
import subprocess

DEFAULTS = {
    "scale": 3.0,
    "ip": "localhost",
    "port": 7860,
    "batch limit": 10,
}


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
    parser.add_argument("--ip", dest="ip", type=str, default=DEFAULTS["ip"],
                        help=f"IP address of the running Stable Diffusion WebUI (default = {DEFAULTS['ip']:s}).")

    parser.add_argument("--port", dest="port", type=int, default=DEFAULTS["port"],
                        help=f"The port of the running Stable Diffusion WebUI (default = {DEFAULTS['port']:d}).")

    parser.add_argument("-s", "--scale", type=float, default=DEFAULTS["scale"],
                        help=f"The scale of the output picture (default = {DEFAULTS['scale']:.1f})")

    parser.add_argument("--batch-limit", type=int, default=DEFAULTS["batch limit"],
                        help=f"The maximum number of frames to be processed in one batch (default = {DEFAULTS['batch limit']:.1f})")

    parser.add_argument("input_video", type=str, help="Path to the video to upscale.")

    # Parse command-line arguments.
    args = parser.parse_args()

    input_video = os.path.realpath(args.input_video)

    input_width, input_height = video_orig_size(input_video)
    if input_width is None:
        raise IOError(f"Cannot specify {input_video:s} original size, the output size must be set manually.")
    output_width = int(float(args.scale) * input_width)
    output_height = int(float(args.scale) * input_height)
    scale = float(args.scale)

    basename, ext = os.path.splitext(input_video)
    output_video = f"{basename:s}_{output_width:d}x{output_height:d}.mp4"

    print(f"Input File:    {input_video:<s}")
    print(f"Output File:   {output_video:<s}")
    print(f"Output Width:  {output_width:<d}")
    print(f"Output Height: {output_height:<d}")

    upscaler = VideoUpscaler(host=str(args.ip), port=int(args.port))
    upscaler.upscale_video(input_video, output_video, scale, batch_limit=args.batch_limit)

