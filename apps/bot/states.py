from aiogram.dispatcher.filters.state import StatesGroup, State


class BotForm(StatesGroup):
    main_menu = State()
    contacts = State()
    anorhome_menu = State()
