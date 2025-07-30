#!/usr/bin/env python3
# ytdx - загрузчик YouTube видео и аудио
# автор Flaymie, 2025

import argparse
import os
import sys
from pathlib import Path
import yt_dlp

def main():
    parser = argparse.ArgumentParser(description="Скачивание видео с YouTube по ссылке")
    parser.add_argument("url", help="Ссылка на видео")
    parser.add_argument("-a", "--audio", action="store_true", help="Скачать только аудио (mp3)")
    parser.add_argument("-f", "--format", help="Формат (mp4, mp3, webm и т.д.)")
    parser.add_argument("-o", "--output", help="Папка для сохранения", default="downloads")
    parser.add_argument("-n", "--name", help="Имя выходного файла (без расширения)")
    parser.add_argument("-q", "--quality", help="Качество видео (1080, 720, 480, 360)")
    
    args = parser.parse_args()
    
    # Создаем папку для загрузок если её нет
    output_dir = Path(args.output)
    output_dir.mkdir(exist_ok=True, parents=True)
    
    # Базовые опции для yt-dlp
    ydl_opts = {
        'paths': {'home': str(output_dir)},
        'quiet': False,
        'no_warnings': False,
        'no_progress': False,
    }
    
    # Опции для аудио
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
    
    # Опции для формата
    if args.format and not args.audio:
        if args.format.lower() == 'mp4':
            format_str = 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best'
        elif args.format.lower() == 'webm':
            format_str = 'bestvideo[ext=webm]+bestaudio[ext=webm]/best[ext=webm]/best'
        else:
            format_str = f'best[ext={args.format.lower()}]/best'
        
        ydl_opts['format'] = format_str
    
    # Опции для качества
    if args.quality and not args.audio:
        quality = args.quality.replace('p', '')
        if quality in ('1080', '720', '480', '360'):
            if args.format and args.format.lower() == 'mp4':
                ydl_opts['format'] = f'bestvideo[height<={quality}][ext=mp4]+bestaudio[ext=m4a]/best[height<={quality}][ext=mp4]/best'
            else:
                ydl_opts['format'] = f'bestvideo[height<={quality}]+bestaudio/best[height<={quality}]/best'
    
    # Настройка имени файла
    if args.name:
        if args.audio:
            ydl_opts['outtmpl'] = {'default': f'{args.name}.%(ext)s'}
        else:
            ext = args.format if args.format else 'mp4'
            ydl_opts['outtmpl'] = {'default': f'{args.name}.{ext}'}
    else:
        ydl_opts['outtmpl'] = {'default': '%(title)s.%(ext)s'}
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            print(f"Начинаю загрузку: {args.url}")
            ydl.download([args.url])
            print(f"Загрузка завершена. Файлы сохранены в: {output_dir}")
    except Exception as e:
        print(f"Ошибка при загрузке: {e}", file=sys.stderr)
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main()) 