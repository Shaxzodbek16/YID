from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)

from app.bot.handlers.admin.channel import get_all_channels
from app.bot.utils.count_ui import num_to_emoji
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
    delete,
)
from typing import Sequence
from app.bot.models.channel import Channel


async def admin_menu(is_superuser: bool = False) -> ReplyKeyboardMarkup:
    rk_btn = [
        [KeyboardButton(text=statistics), KeyboardButton(text=all_users)],
        [KeyboardButton(text=youtube_info), KeyboardButton(text=instagram_info)],
        [KeyboardButton(text=channels_btn)],
    ]
    if is_superuser:
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


async def file_format_for_downloads(text: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="📊 Export as Excel (XLSX)",
                    callback_data=FileType.XLSX.value + text,
                ),
            ],
            [
                InlineKeyboardButton(
                    text="📄 Export as CSV",
                    callback_data=FileType.CSV.value + text,
                ),
            ],
            [
                InlineKeyboardButton(
                    text="📦 Export All Formats",
                    callback_data=FileType.ALL_FORMAT.value + text,
                ),
            ],
        ]
    )


async def channels_list() -> InlineKeyboardMarkup:
    in_kyb = []
    channels: Sequence[Channel] = await get_all_channels()
    for idx, i in enumerate(channels, start=1):
        in_kyb.append(
            [
                InlineKeyboardButton(
                    text=f"{await num_to_emoji(idx)}",
                    callback_data=f"channel:{i.channel_name}",
                ),
                InlineKeyboardButton(
                    text=f"{i.channel_name}",
                    url=i.channel_link,
                    callback_data=f"channel:{i.channel_name}",
                ),
                InlineKeyboardButton(
                    text=delete,
                    callback_data=f"{delete_channel}:{i.channel_name}:{i.id}",
                ),
            ]
        )
    return InlineKeyboardMarkup(inline_keyboard=in_kyb)


async def channel_confirm(name: str, channel_id: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Yes", callback_data=f"confirm_delete:{name}:{channel_id}"
                ),
                InlineKeyboardButton(
                    text="No", callback_data=f"cancel_delete:{name}:{channel_id}"
                ),
            ]
        ]
    )
