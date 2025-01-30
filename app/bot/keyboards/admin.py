from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def admin_main_menu() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="Get all channels"),
                KeyboardButton(text="Get all users"),
            ],
            [
                KeyboardButton(text="Send message"),
            ],
        ],
        resize_keyboard=True,
        one_time_keyboard=True,
    )
