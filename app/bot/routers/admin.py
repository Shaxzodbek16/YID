import os
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, FSInputFile
from app.bot.constants.admin import (
    all_users,
    channels_btn,
    back_to_main_menu,
    statistics,
)
from app.bot.filters.admin_or_superuser import IsSuperuserOrAdmin
from app.bot.keyboards.admin import file_format, chanel_control_btn, admin_menu
from app.bot.models import User
from app.bot.routers.help import start
from app.bot.utils.enums import FileType
from app.bot.utils.generate_files import export_model_to_file
from app.bot.utils.statistics_data import statistics_data

router = Router()


async def remove_file(file_path: str):
    if os.path.exists(file_path):
        os.remove(file_path)


@router.message(IsSuperuserOrAdmin(), F.text == all_users)
async def get_all_users(message: Message):
    await message.answer(
        "📂 <b>Select the file format</b> to export all users:\n"
        "• <b>CSV</b> – for easy text-based data handling.\n"
        "• <b>XLSX</b> – for detailed Excel formatting.\n"
        "\nPlease choose an option below: ⬇️",
        reply_markup=await file_format(),
        parse_mode="HTML",
    )


@router.callback_query(IsSuperuserOrAdmin(), F.data == FileType.CSV.value)
async def get_all_users_as_csv(callback: CallbackQuery):
    await callback.message.answer("⏳ Preparing CSV file...")
    try:
        file_path = await export_model_to_file(User, FileType.CSV)
        await callback.message.answer("⏳ Preparing CSV file...")
        file_path = os.path.abspath(file_path)
        document = FSInputFile(file_path)

        await callback.message.answer_document(
            document=document,
            caption="✅ <b>CSV file is ready!</b>\n"
            "📄 <i>Download the list of users below:</i>",
            parse_mode="HTML",
        )
        await remove_file(file_path)
    except Exception as e:
        await callback.message.answer(
            f"❌ <b>Failed to generate CSV file.</b>\n" f"🔍 <i>Reason: {str(e)}</i>",
            parse_mode="HTML",
        )
    finally:
        pass


@router.callback_query(IsSuperuserOrAdmin(), F.data == FileType.XLSX.value)
async def get_all_users_as_xlsx(callback: CallbackQuery):
    await callback.message.answer("⏳ Preparing Exec file...")
    try:
        file_path = await export_model_to_file(User, FileType.XLSX)
        file_path = os.path.abspath(file_path)
        document = FSInputFile(file_path)
        await callback.message.answer("⏳ Uploading Excel file...")
        await callback.message.answer_document(
            document=document,
            caption="📊 <b>Excel file is ready!</b>\n"
            "🔍 <i>Open it for a well-structured user list.</i>",
            parse_mode="HTML",
        )
        await remove_file(file_path)
    except Exception as e:
        await callback.message.answer(
            f"❌ <b>Failed to generate Excel file.</b>\n" f"🔍 <i>Reason: {str(e)}</i>",
            parse_mode="HTML",
        )
    finally:
        pass


@router.callback_query(IsSuperuserOrAdmin(), F.data == FileType.ALL_FORMAT.value)
async def get_all_users_as_all(callback: CallbackQuery):
    await get_all_users_as_xlsx(callback)
    await get_all_users_as_csv(callback)
    await callback.message.delete()
    await callback.message.answer(
        "✅ <b>All files are ready!</b>\n"
        "📄 <i>You can now download both CSV and Excel files.</i>",
        parse_mode="HTML",
    )


@router.message(F.text == channels_btn)
async def chanel_control(message: Message):
    await message.answer(
        "📡 <b>Channel Management</b>",
        reply_markup=await chanel_control_btn(),
        parse_mode="HTML",
    )


@router.message(IsSuperuserOrAdmin(), F.text == back_to_main_menu)
async def back_to_main_menu(message: Message):
    await message.answer("🔙 <b>Back to Main Menu</b>", reply_markup=await admin_menu())


@router.message(IsSuperuserOrAdmin(), F.text == statistics)
async def get_statistics(message: Message):
    await message.answer(await statistics_data(), parse_mode="HTML")
