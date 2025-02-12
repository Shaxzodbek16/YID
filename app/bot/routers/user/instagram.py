import asyncio
import os
import re

from aiogram import Router, F
from aiogram.enums.chat_action import ChatAction
from aiogram.types import Message, FSInputFile, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from app.bot.constants.users import instagram_btn
from app.bot.handlers.user.download_instagram import (
    download_instagram,
    download_instagram_audio,
)
from app.bot.keyboards.user import insta_option_inline
from app.bot.utils.enums import VideoType
from app.bot.handlers.user.downloads import create_downloads

router = Router()


class InstagramState(StatesGroup):
    instagram_link = State()


@router.message(F.text == instagram_btn)
async def handle_instagram_button(message: Message, state: FSMContext):
    """
    Ask the user for the Instagram post link.
    """
    await message.answer(
        "📷 <b>Instagram Download</b>\n\n"
        "Please send me the Instagram post link you'd like to download. "
        "Make sure it's a valid Instagram URL (e.g., https://www.instagram.com/... )",
        parse_mode="HTML",
    )
    await state.set_state(InstagramState.instagram_link)


@router.message(InstagramState.instagram_link)
async def handle_instagram_link(message: Message, state: FSMContext):
    """
    Validate the user's provided Instagram link, or prompt again if it's invalid.
    """
    link = message.text
    if not link:
        await message.answer(
            "⚠️ <b>No link received.</b>\n\n"
            "Please send a valid Instagram post link so I can download it for you.",
            parse_mode="HTML",
        )
        return
    if not re.match(r"^https://www\.instagram\.com/", link):
        await message.answer(
            "❌ <b>Invalid link format.</b>\n\n"
            "It doesn’t look like a valid Instagram post link. "
            "Please try again with a correct URL (e.g., https://www.instagram.com/p/...).",
            parse_mode="HTML",
        )
        return

    await state.update_data(link=link)
    await message.answer(
        "✅ <b>Link received!</b>\n\n" "Now, choose the download format below:",
        reply_markup=await insta_option_inline(),
        parse_mode="HTML",
    )


async def send_video_with_retries(
    message: Message, video: FSInputFile, caption: str, retries=3, delay=2
):
    """
    Attempt sending video multiple times with retries in case of network issues.
    """
    for attempt in range(retries):
        try:
            await message.answer_video(video, caption=caption)
            return
        except Exception as e:
            print(f"Attempt {attempt + 1} failed: {e}")
            if attempt < retries - 1:
                await asyncio.sleep(delay)
            else:
                raise e


@router.callback_query(F.data.startswith("instagram_format:"))
async def instagram_download_mp3(callback: CallbackQuery, state: FSMContext):
    link = (await state.get_data()).get("link")
    format_ = callback.data.split(":")[-1]
    cookies_path = os.path.abspath(
        os.path.join("media", "cookies", "www.instagram.com_cookies.txt")
    )

    filename = f"{callback.from_user.id}_instagram"
    media_path = os.path.abspath(os.path.join("media"))

    # Let the user know we're about to start the download
    await callback.answer("⏳ <b>Starting your download...</b>", show_alert=False)
    await create_downloads(callback.from_user.id, link, VideoType.INSTAGRAM, format_)

    if format_ == "mp4":
        # Download MP4 (video)
        try:
            await callback.message.bot.send_chat_action(
                callback.message.chat.id, ChatAction.UPLOAD_VIDEO
            )
            await download_instagram(filename, link, cookies_path, media_path)

            # Prepare and send the video file
            file_path = os.path.join(media_path, filename + ".mp4")
            file = FSInputFile(file_path)
            await callback.message.answer_video(
                video=file,
                caption="🎬 <b>Your video is ready!</b>\n\nEnjoy your download. 📥",
                supports_streaming=True,
                parse_mode="HTML",
            )
        except Exception as e:
            await callback.message.answer(
                f"❌ <b>Error downloading video.</b>\n\n<i>Details: {str(e)}</i>",
                parse_mode="HTML",
            )
            print(f"Error: {e}")
        finally:
            # Cleanup file and state
            await state.clear()
            try:
                os.remove(os.path.join(media_path, filename + ".mp4"))
            except OSError:
                pass
            await callback.message.delete_reply_markup()

    elif format_ == "mp3":
        # Download MP3 (audio)
        try:
            await callback.message.bot.send_chat_action(
                callback.message.chat.id, ChatAction.UPLOAD_VOICE
            )
            await download_instagram_audio(filename, link, cookies_path, media_path)

            # Prepare and send the audio file
            file_path = os.path.join(media_path, filename + ".mp3")
            file = FSInputFile(file_path)
            await callback.message.answer_audio(
                audio=file,
                caption="🎵 <b>Your audio file is ready!</b>\n\nEnjoy your download. 📥",
                parse_mode="HTML",
            )
        except Exception as e:
            await callback.message.answer(
                f"❌ <b>Error downloading audio.</b>\n\n<i>Details: {str(e)}</i>",
                parse_mode="HTML",
            )
            print(f"Error: {e}")
        finally:
            # Cleanup file and state
            await state.clear()
            try:
                os.remove(os.path.join(media_path, filename + ".mp3"))
            except OSError:
                pass
            await callback.message.delete_reply_markup()
