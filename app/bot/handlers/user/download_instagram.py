from smdpy.social.instagram import Instagram


async def download_instagram(
    name: str, url: str, cookies_path: str, output_path: str = None
):
    instagram = Instagram(url=url, cookie_file_path=cookies_path)
    return instagram.download_video(name=name, path=output_path)


async def download_instagram_audio(
    name: str, url: str, cookies_path: str, output_path: str = None
):
    instagram = Instagram(url=url, cookie_file_path=cookies_path)
    return instagram.download_audio_mp3(name=name, path=output_path)
