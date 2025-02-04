import os

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, FSInputFile
from aiogram.enums.chat_action import ChatAction

from app.bot.constants.admin import (
    all_users,
    channels_btn,
    back_to_main_menu,
    statistics,
    youtube_info,
    instagram_info,
    channels_info,
    delete_channel,
)
from app.bot.filters.admin_or_superuser import IsSuperuserOrAdmin
from app.bot.handlers.admin.channel import delete_channel_by_id
from app.bot.keyboards.admin import (
    file_format,
    chanel_control_btn,
    admin_menu,
    file_format_for_downloads,
    channels_list,
    channel_confirm,
)
from app.bot.models import User
from app.bot.utils.downloads_info import get_downloads_info
from app.bot.utils.enums import FileType
from app.bot.utils.generate_files import export_model_to_file
from app.bot.utils.statistics_data import statistics_data

router = Router()


async def remove_file(file_path: str):
    """Safely remove a file if it exists."""
    if os.path.exists(file_path):
        os.remove(file_path)


@router.message(IsSuperuserOrAdmin(), F.text == all_users)
async def get_all_users(message: Message):
    """
    Prompt the admin to select a file format (CSV or XLSX)
    for exporting the list of users.
    """
    await message.answer(
        "📂 <b>Export All Users</b>\n\n"
        "Choose a file format below:\n"
        "• <b>CSV</b> – Easy to handle in text-based applications.\n"
        "• <b>XLSX</b> – Perfect for Excel or similar tools.\n\n"
        "Please pick one:",
        reply_markup=await file_format(),
        parse_mode="HTML",
    )


@router.callback_query(IsSuperuserOrAdmin(), F.data == FileType.CSV.value)
async def get_all_users_as_csv(callback: CallbackQuery):
    """Generate and send the CSV file of all users."""
    await callback.message.answer("⏳ Please wait, generating CSV file...")
    await callback.message.bot.send_chat_action(
        chat_id=callback.message.chat.id, action=ChatAction.UPLOAD_DOCUMENT
    )
    try:
        file_path = await export_model_to_file(User, FileType.CSV)
        file_path = os.path.abspath(file_path)
        document = FSInputFile(file_path)

        await callback.message.bot.send_chat_action(
            chat_id=callback.message.chat.id, action=ChatAction.UPLOAD_DOCUMENT
        )
        await callback.message.answer_document(
            document=document,
            caption=(
                "✅ <b>Your CSV file is ready!</b>\n"
                "📄 <i>You can download the user list below.</i>"
            ),
            parse_mode="HTML",
        )
        await remove_file(file_path)
    except Exception as e:
        await callback.message.answer(
            f"❌ <b>Couldn’t generate CSV file.</b>\n" f"🔍 <i>Reason: {str(e)}</i>",
            parse_mode="HTML",
        )


@router.callback_query(IsSuperuserOrAdmin(), F.data == FileType.XLSX.value)
async def get_all_users_as_xlsx(callback: CallbackQuery):
    """Generate and send the XLSX (Excel) file of all users."""
    await callback.message.answer("⏳ Please wait, generating Excel file...")
    await callback.message.bot.send_chat_action(
        chat_id=callback.message.chat.id, action=ChatAction.UPLOAD_DOCUMENT
    )
    try:
        file_path = await export_model_to_file(User, FileType.XLSX)
        file_path = os.path.abspath(file_path)
        document = FSInputFile(file_path)

        await callback.message.bot.send_chat_action(
            chat_id=callback.message.chat.id, action=ChatAction.UPLOAD_DOCUMENT
        )
        await callback.message.answer_document(
            document=document,
            caption=(
                "📊 <b>Your Excel file is ready!</b>\n"
                "🔍 <i>Open it to view a well-structured user list.</i>"
            ),
            parse_mode="HTML",
        )
        await remove_file(file_path)
    except Exception as e:
        await callback.message.answer(
            f"❌ <b>Couldn’t generate Excel file.</b>\n" f"🔍 <i>Reason: {str(e)}</i>",
            parse_mode="HTML",
        )


@router.callback_query(IsSuperuserOrAdmin(), F.data == FileType.ALL_FORMAT.value)
async def get_all_users_as_all(callback: CallbackQuery):
    """
    Generate and send both CSV and XLSX versions of user data.
    Then display a final message when both are done.
    """
    await get_all_users_as_xlsx(callback)
    await get_all_users_as_csv(callback)
    await callback.message.delete()
    await callback.message.answer(
        "✅ <b>All files are ready!</b>\n"
        "📄 <i>You can now download both the CSV and Excel files.</i>",
        parse_mode="HTML",
    )


@router.message(F.text == channels_btn)
async def chanel_control(message: Message):
    """
    Display the Channel Management menu.
    """
    await message.answer(
        "📡 <b>Channel Management Menu</b>\n"
        "Use the options below to manage your channels:",
        reply_markup=await chanel_control_btn(),
        parse_mode="HTML",
    )


@router.message(IsSuperuserOrAdmin(), F.text == back_to_main_menu)
async def back_to_main_menu_handler(message: Message):
    """Go back to the main admin menu."""
    await message.answer(
        "🔙 <b>Back to the Admin Main Menu</b>",
        reply_markup=await admin_menu(),
    )


@router.message(IsSuperuserOrAdmin(), F.text == statistics)
async def get_statistics(message: Message):
    """
    Show overall statistics to the admin.
    """
    stats = await statistics_data()
    await message.answer(stats, parse_mode="HTML")


@router.message(IsSuperuserOrAdmin(), F.text == youtube_info)
async def get_all_info_youtube(message: Message):
    """
    Prompt for exporting YouTube-specific download info (CSV or XLSX).
    """
    await message.answer(
        "📂 <b>Export YouTube Download Info</b>\n\n"
        "Choose a file format below:\n"
        "• <b>CSV</b> – Easy text-based format.\n"
        "• <b>XLSX</b> – Suited for spreadsheet apps.\n\n"
        "Please pick one:",
        reply_markup=await file_format_for_downloads("youtube"),
        parse_mode="HTML",
    )


@router.callback_query(IsSuperuserOrAdmin(), F.data == FileType.CSV.value + "youtube")
async def get_all_youtube_as_csv(callback: CallbackQuery):
    """Generate YouTube download info as a CSV file."""
    await callback.message.answer("⏳ Please wait, generating CSV file...")
    await callback.message.bot.send_chat_action(
        chat_id=callback.message.chat.id, action=ChatAction.UPLOAD_DOCUMENT
    )
    try:
        file_path = await get_downloads_info(youtube=True, csv=True)
        file_path = os.path.abspath(file_path)
        document = FSInputFile(file_path)

        await callback.message.bot.send_chat_action(
            chat_id=callback.message.chat.id, action=ChatAction.UPLOAD_DOCUMENT
        )
        await callback.message.answer_document(
            document=document,
            caption=(
                "✅ <b>CSV file is ready!</b>\n"
                "📄 <i>Click below to download YouTube download info.</i>"
            ),
            parse_mode="HTML",
        )
        await remove_file(file_path)
    except Exception as e:
        await callback.message.answer(
            f"❌ <b>Couldn’t generate CSV file.</b>\n" f"🔍 <i>Reason: {str(e)}</i>",
            parse_mode="HTML",
        )


@router.callback_query(IsSuperuserOrAdmin(), F.data == FileType.XLSX.value + "youtube")
async def get_all_youtube_as_xlsx(callback: CallbackQuery):
    """Generate YouTube download info as an Excel file."""
    await callback.message.answer("⏳ Please wait, generating Excel file...")
    await callback.message.bot.send_chat_action(
        chat_id=callback.message.chat.id, action=ChatAction.UPLOAD_DOCUMENT
    )
    try:
        file_path = await get_downloads_info(youtube=True, xlsx=True)
        file_path = os.path.abspath(file_path)
        document = FSInputFile(file_path)

        await callback.message.bot.send_chat_action(
            chat_id=callback.message.chat.id, action=ChatAction.UPLOAD_DOCUMENT
        )
        await callback.message.answer_document(
            document=document,
            caption=(
                "📊 <b>Excel file is ready!</b>\n"
                "🔍 <i>View a well-structured YouTube info list.</i>"
            ),
            parse_mode="HTML",
        )
        await remove_file(file_path)
    except Exception as e:
        await callback.message.answer(
            f"❌ <b>Couldn’t generate Excel file.</b>\n" f"🔍 <i>Reason: {str(e)}</i>",
            parse_mode="HTML",
        )


@router.callback_query(
    IsSuperuserOrAdmin(), F.data == FileType.ALL_FORMAT.value + "youtube"
)
async def get_all_youtube_as_all(callback: CallbackQuery):
    """Generate both CSV and Excel for YouTube info, then notify the admin."""
    await get_all_youtube_as_csv(callback)
    await get_all_youtube_as_xlsx(callback)
    await callback.message.delete()
    await callback.message.answer(
        "✅ <b>All YouTube files are ready!</b>\n"
        "📄 <i>You can now download both CSV and Excel files.</i>",
        parse_mode="HTML",
    )


@router.message(IsSuperuserOrAdmin(), F.text == instagram_info)
async def get_all_info_instagram(message: Message):
    """
    Prompt for exporting Instagram-specific download info (CSV or XLSX).
    """
    await message.answer(
        "📂 <b>Export Instagram Download Info</b>\n\n"
        "Choose a file format below:\n"
        "• <b>CSV</b> – Easy text-based format.\n"
        "• <b>XLSX</b> – Suited for spreadsheet apps.\n\n"
        "Please pick one:",
        reply_markup=await file_format_for_downloads("instagram"),
        parse_mode="HTML",
    )


@router.callback_query(IsSuperuserOrAdmin(), F.data == FileType.CSV.value + "instagram")
async def get_all_instagram_as_csv(callback: CallbackQuery):
    """Generate Instagram download info as a CSV file."""
    await callback.message.answer("⏳ Please wait, generating CSV file...")
    try:
        file_path = await get_downloads_info(instagram=True, csv=True)
        file_path = os.path.abspath(file_path)
        document = FSInputFile(file_path)

        await callback.message.answer_document(
            document=document,
            caption=(
                "✅ <b>CSV file is ready!</b>\n"
                "📄 <i>Click below to download Instagram download info.</i>"
            ),
            parse_mode="HTML",
        )
        await remove_file(file_path)
    except Exception as e:
        await callback.message.answer(
            f"❌ <b>Couldn’t generate CSV file.</b>\n" f"🔍 <i>Reason: {str(e)}</i>",
            parse_mode="HTML",
        )


@router.callback_query(
    IsSuperuserOrAdmin(), F.data == FileType.XLSX.value + "instagram"
)
async def get_all_instagram_as_xlsx(callback: CallbackQuery):
    """Generate Instagram download info as an Excel file."""
    await callback.message.answer("⏳ Please wait, generating Excel file...")
    try:
        file_path = await get_downloads_info(instagram=True, xlsx=True)
        file_path = os.path.abspath(file_path)
        document = FSInputFile(file_path)

        await callback.message.answer_document(
            document=document,
            caption=(
                "📊 <b>Excel file is ready!</b>\n"
                "🔍 <i>View a well-structured Instagram info list.</i>"
            ),
            parse_mode="HTML",
        )
        await remove_file(file_path)
    except Exception as e:
        await callback.message.answer(
            f"❌ <b>Couldn’t generate Excel file.</b>\n" f"🔍 <i>Reason: {str(e)}</i>",
            parse_mode="HTML",
        )


@router.callback_query(
    IsSuperuserOrAdmin(), F.data == FileType.ALL_FORMAT.value + "instagram"
)
async def get_all_instagram_as_all(callback: CallbackQuery):
    """Generate both CSV and Excel for Instagram info, then notify the admin."""
    await get_all_instagram_as_csv(callback)
    await get_all_instagram_as_xlsx(callback)
    await callback.message.delete()
    await callback.message.answer(
        "✅ <b>All Instagram files are ready!</b>\n"
        "📄 <i>You can now download both CSV and Excel files.</i>",
        parse_mode="HTML",
    )


@router.message(IsSuperuserOrAdmin(), F.text == channels_info)
async def get_channels_info(message: Message):
    """Show the list of available channels."""
    await message.answer(
        "🗂 <b>Available Channels</b>\n"
        "Below is the list of channels currently managed:",
        reply_markup=await channels_list(),
        parse_mode="HTML",
    )


@router.callback_query(
    IsSuperuserOrAdmin(), lambda c: c.data.startswith(f"{delete_channel}:")
)
async def process_delete_button(callback_query: CallbackQuery):
    """
    Ask for confirmation before deleting a channel.
    """
    channel_name = callback_query.data.split(":")[-2]
    channel_id = callback_query.data.split(":")[-1]
    await callback_query.message.edit_text(
        text=(
            f"❓ Are you sure you want to delete the <b>{channel_name}</b> channel?\n"
            "This action cannot be undone!"
        ),
        reply_markup=await channel_confirm(channel_name, channel_id),
    )


@router.callback_query(
    IsSuperuserOrAdmin(), lambda c: c.data.startswith("confirm_delete:")
)
async def process_confirm_delete(callback_query: CallbackQuery):
    """Perform channel deletion after confirmation."""
    await callback_query.message.bot.send_chat_action(
        chat_id=callback_query.message.chat.id, action=ChatAction.TYPING
    )
    channel_id = callback_query.data.split(":")[-1]
    channel_name = callback_query.data.split(":")[-2]
    await delete_channel_by_id(int(channel_id))
    await callback_query.message.edit_text(
        text=(
            f"✅ <b>{channel_name}</b> has been successfully deleted.\n\n"
            "🗂 <b>Updated Channel List</b>\n"
            "Check out the remaining channels below:"
        ),
        reply_markup=await channels_list(),
    )


@router.callback_query(
    IsSuperuserOrAdmin(), lambda c: c.data.startswith("cancel_delete:")
)
async def process_cancel_delete(callback_query: CallbackQuery):
    """
    Cancel channel deletion and show the channel list again.
    """
    await callback_query.message.delete()
    channel_name = callback_query.data.split(":")[-2]
    await callback_query.message.answer(
        f"❌ Deletion canceled for <b>{channel_name}</b>.\n"
        "Returning you to the channel list below:",
        reply_markup=await channels_list(),
        parse_mode="HTML",
    )
