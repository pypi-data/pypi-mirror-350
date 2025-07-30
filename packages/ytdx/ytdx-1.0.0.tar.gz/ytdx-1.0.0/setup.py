from setuptools import setup

setup(
    name="ytdx",
    version="1.0.0",
    description="YouTube video downloader via command line",
    author="Flaymie",
    author_email="funquenop@gmail.com",
    url="https://github.com/Flaymie/ytdx",
    py_modules=["ytdx"],
    install_requires=[
        "yt-dlp",
    ],
    entry_points={
        "console_scripts": [
            "ytdx=ytdx:main",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
) 