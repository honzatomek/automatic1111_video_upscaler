from setuptools import setup, find_packages

setup(
    name="video_upscaler",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "ffmpeg-python",
        "Pillow",
        "webuiapi",
    ],
    author="Dalton Bailey",
    author_email="drbailey117@example.com",
    description="A package for resizing videos using Automatic1111 web UI",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/Yalton/video_upscaler",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
)