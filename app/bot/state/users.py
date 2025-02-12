from aiogram.fsm.state import StatesGroup, State


class AddChanel(StatesGroup):
    chanel_name = State()
    chanel_link = State()


class InstagramState(StatesGroup):
    instagram_link = State()


class YouTubeStates(StatesGroup):
    waiting_for_url = State()
    waiting_for_resolution_choice = State()
