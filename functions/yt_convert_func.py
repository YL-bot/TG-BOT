# по ссылке из ютуба возвращает

from pytube import YouTube
import os


# надо запускать скрипт специальный для норм работы, ну на 21.03.23 пока так

def yt_convert(link):
    yt = YouTube(link)

    video = yt.streams.filter(only_audio=True).first()

    out_file = video.download(output_path=".")

    base, ext = os.path.splitext(out_file)
    new_file = base + '.mp3'

    os.rename(out_file, new_file)

    # os.remove(new_file) надо будет обязательно добавить 

# yt_convert('https://www.youtube.com/watch?v=rD7VpUIBi3o')
