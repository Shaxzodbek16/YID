import os

from smdpy.social.youtube import YouTube


class DownloadYouTube:
    def __init__(self, url, out_path, name):
        self.youtube: YouTube = YouTube(url)
        self.out_path = out_path
        self.name = name

    async def get_resolutions(self):
        return self.youtube.get_available_resolutions()

    async def download(self, resolution):
        return self.youtube.download_video(self.out_path, self.name, resolution)

    async def download_audio(self):
        return self.youtube.download_audio_mp3(self.out_path, self.name)


async def check_file_size(path: str, size):
    return os.path.getsize(path) / 1024 / 1024 < size
