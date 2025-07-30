#!/usr/bin/env python3

import argparse
import os
import sys
from pathlib import Path
import yt_dlp

def main():
    parser = argparse.ArgumentParser(description="Download videos from YouTube by URL")
    parser.add_argument("url", help="Video URL")
    parser.add_argument("-a", "--audio", action="store_true", help="Download audio only (mp3)")
    parser.add_argument("-f", "--format", help="Format (mp4, mp3, webm, etc)")
    parser.add_argument("-o", "--output", help="Output directory", default=".")
    parser.add_argument("-n", "--name", help="Output filename (without extension)")
    parser.add_argument("-q", "--quality", help="Video quality (1080, 720, 480, 360)")
    
    args = parser.parse_args()
    
    if args.output.startswith('~'):
        output_dir = Path(os.path.expanduser(args.output))
    elif args.output.startswith('/'):
        output_dir = Path(args.output)
    else:
        output_dir = Path(os.getcwd()) / args.output
    
    output_dir.mkdir(exist_ok=True, parents=True)
    
    ydl_opts = {
        'quiet': False,
        'no_warnings': False,
        'no_progress': False,
    }
    
    if args.audio:
        ydl_opts.update({
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        })
        if not args.format:
            args.format = 'mp3'
    
    if args.format and not args.audio:
        if args.format.lower() == 'mp4':
            format_str = 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best'
        elif args.format.lower() == 'webm':
            format_str = 'bestvideo[ext=webm]+bestaudio[ext=webm]/best[ext=webm]/best'
        else:
            format_str = f'best[ext={args.format.lower()}]/best'
        
        ydl_opts['format'] = format_str
    
    if args.quality and not args.audio:
        quality = args.quality.replace('p', '')
        if quality in ('1080', '720', '480', '360'):
            if args.format and args.format.lower() == 'mp4':
                ydl_opts['format'] = f'bestvideo[height<={quality}][ext=mp4]+bestaudio[ext=m4a]/best[height<={quality}][ext=mp4]/best'
            else:
                ydl_opts['format'] = f'bestvideo[height<={quality}]+bestaudio/best[height<={quality}]/best'
    
    file_path = output_dir
    if args.name:
        if args.audio:
            filename = f'{args.name}.%(ext)s'
        else:
            ext = args.format if args.format else 'mp4'
            filename = f'{args.name}.{ext}'
    else:
        filename = '%(title)s.%(ext)s'
    
    ydl_opts['outtmpl'] = {'default': str(file_path / filename)}
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            print(f"Starting download: {args.url}")
            ydl.download([args.url])
            print(f"Download complete. Files saved to: {output_dir}")
    except Exception as e:
        print(f"Download error: {e}", file=sys.stderr)
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main()) 