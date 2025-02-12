import asyncio
import os
from aiogram import Router, Bot, F, types
from aiogram.filters.callback_data import CallbackData
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.enums.chat_action import ChatAction

from app.bot.constants.users import youtube_btn
from app.bot.handlers.user.download_youtube import DownloadYouTube, check_file_size
from app.bot.handlers.user.downloads import create_downloads
from app.bot.state.users import YouTubeStates
from app.bot.utils.enums import VideoType


class ResolutionCallback(CallbackData, prefix="yt_res"):
    resolution: str


router = Router()


@router.message(F.text == youtube_btn)
async def cmd_youtube(message: Message, state: FSMContext):
    await message.answer("Please send me the YouTube link:")
    await state.set_state(YouTubeStates.waiting_for_url)


@router.message(YouTubeStates.waiting_for_url)
async def process_youtube_url(message: Message, state: FSMContext):
    youtube_url = message.text.strip()

    if not (youtube_url.startswith("http://") or youtube_url.startswith("https://")):
        await message.answer("That doesn't look like a valid URL. Try again.")
        return
    file_name = f"{message.from_user.id}_youtube_video"
    media_path = os.path.abspath(os.path.join("media"))
    downloader = DownloadYouTube(url=youtube_url, out_path=media_path, name=file_name)

    try:
        resolutions = await downloader.get_resolutions()
    except Exception as e:
        await message.answer(f"Failed to get resolutions: {e}")
        return

    keyboard_buttons = []
    for res in resolutions:
        keyboard_buttons.append(
            [
                InlineKeyboardButton(
                    text=f"{res}",
                    callback_data=ResolutionCallback(resolution=res).pack(),
                )
            ]
        )

    keyboard_buttons.append(
        [
            InlineKeyboardButton(
                text="MP3 (audio)",
                callback_data=ResolutionCallback(resolution="mp3").pack(),
            )
        ]
    )

    markup = InlineKeyboardMarkup(inline_keyboard=keyboard_buttons)

    await state.update_data(
        youtube_url=youtube_url, download_path=media_path, file_name=file_name
    )
    await message.answer("Select a resolution or MP3:", reply_markup=markup)
    await state.set_state(YouTubeStates.waiting_for_resolution_choice)


@router.callback_query(
    YouTubeStates.waiting_for_resolution_choice, ResolutionCallback.filter()
)
async def process_resolution_choice(
    callback_query: types.CallbackQuery,
    callback_data: ResolutionCallback,
    state: FSMContext,
    bot: Bot,
):
    data = await state.get_data()
    youtube_url = data["youtube_url"]
    download_path = data["download_path"]
    file_name = data["file_name"]

    downloader = DownloadYouTube(youtube_url, download_path, file_name)

    resolution_chosen = callback_data.resolution
    await callback_query.message.answer(f"Downloading video in {resolution_chosen}...")

    try:
        if resolution_chosen == "mp3":
            res = await downloader.download_audio()
            file_location = res["filepath"]
        else:
            res = await downloader.download(resolution_chosen)
            file_location = res["filepath"]
    except Exception as e:
        await callback_query.message.answer(f"Download failed: {e}")
        return

    if await check_file_size(file_location, 50):
        if resolution_chosen == "mp3":
            await callback_query.message.bot.send_chat_action(
                chat_id=callback_query.message.chat.id, action=ChatAction.UPLOAD_VOICE
            )
            await callback_query.message.answer_audio(
                audio=types.FSInputFile(file_location),
                caption="Here is your MP3 audio.",
            )
            os.remove(file_location)
        else:
            await callback_query.message.bot.send_chat_action(
                chat_id=callback_query.message.chat.id, action=ChatAction.UPLOAD_VIDEO
            )
            await asyncio.sleep(2)
            await callback_query.message.answer_video(
                video=types.FSInputFile(file_location),
                caption=f"Here is your video in {resolution_chosen}.",
                supports_streaming=True,
            )
            await asyncio.sleep(5)
            os.remove(file_location)
    else:
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="Download from Website",
                        url="https://trendify.shaxzodbek.com/docs",
                    )
                ]
            ]
        )
        await callback_query.message.answer(
            "File is too large to send via Telegram (over 2GB).", reply_markup=keyboard
        )
    await create_downloads(
        user_id=callback_query.from_user.id,
        url=youtube_url,
        type_=VideoType.YOUTUBE.value,
        format_=resolution_chosen,
    )

    await state.clear()
