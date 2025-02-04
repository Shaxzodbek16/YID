# app/bot/keyboards/user.py

from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)
from app.bot.constants.users import instagram_btn, youtube_btn


async def user_step_1() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=instagram_btn), KeyboardButton(text=youtube_btn)]
        ],
        resize_keyboard=True,
    )


async def format_keyboard() -> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="🎥 MP4", callback_data="format:mp4"),
                InlineKeyboardButton(text="🎵 MP3", callback_data="format:mp3"),
            ]
        ]
    )
    return kb


async def insta_option_inline() -> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🎥 MP4", callback_data="instagram_format:mp4"
                ),
                InlineKeyboardButton(
                    text="🎵 MP3", callback_data="instagram_format:mp3"
                ),
            ]
        ]
    )
    return kb
