from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)
from app.bot.utils.enums import FileType
from app.bot.constants.admin import (
    instagram_info,
    all_users,
    youtube_info,
    channels_info,
    add_admin,
    add_channel,
    update_channel,
    delete_channel,
    delete_admin,
    statistics,
    channels_btn,
    back_to_main_menu,
)


async def admin_menu(is_admin: bool = False) -> ReplyKeyboardMarkup:
    rk_btn = [
        [KeyboardButton(text=statistics), KeyboardButton(text=all_users)],
        [KeyboardButton(text=youtube_info), KeyboardButton(text=instagram_info)],
        [KeyboardButton(text=channels_btn)],
    ]
    if is_admin:
        rk_btn.append(
            [
                KeyboardButton(text=add_admin),
                KeyboardButton(text=delete_admin),
            ]
        )
    return ReplyKeyboardMarkup(keyboard=rk_btn, resize_keyboard=True)


async def chanel_control_btn() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=channels_info), KeyboardButton(text=add_channel)],
            [KeyboardButton(text=update_channel), KeyboardButton(text=delete_channel)],
            [KeyboardButton(text=back_to_main_menu)],
        ],
        resize_keyboard=True,
    )


async def file_format() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="📊 Export as Excel (XLSX)", callback_data=FileType.XLSX.value
                ),
            ],
            [
                InlineKeyboardButton(
                    text="📄 Export as CSV", callback_data=FileType.CSV.value
                ),
            ],
            [
                InlineKeyboardButton(
                    text="📦 Export All Formats",
                    callback_data=FileType.ALL_FORMAT.value,
                ),
            ],
        ]
    )


async def file_format_youtube() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="📊 Export as Excel (XLSX)",
                    callback_data=FileType.XLSX.value + "youtube",
                ),
            ],
            [
                InlineKeyboardButton(
                    text="📄 Export as CSV",
                    callback_data=FileType.CSV.value + "youtube",
                ),
            ],
            [
                InlineKeyboardButton(
                    text="📦 Export All Formats",
                    callback_data=FileType.ALL_FORMAT.value + "youtube",
                ),
            ],
        ]
    )
