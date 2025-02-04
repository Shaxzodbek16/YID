from aiogram.fsm.state import StatesGroup, State


class AddChanel(StatesGroup):
    chanel_name = State()
    chanel_link = State()


class InstagramState(StatesGroup):
    instagram_link = State()
