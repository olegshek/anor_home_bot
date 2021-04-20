from aiogram.dispatcher.filters.state import StatesGroup, State


class CustomerForm(StatesGroup):
    language_choice = State()
    phone_number = State()
    full_name = State()


class LeadForm(StatesGroup):
    project_type = State()
    project_choice = State()
    project_menu = State()
    room_quantity_or_floor_number_choice = State()
    square_choice = State()
    project_object_choice = State()
    cart = State()
