from aiogram.dispatcher.filters.state import StatesGroup, State


class CompanyForm(StatesGroup):
    menu = State()
    about = State()
    services = State()
    vacancies = State()
    service_detail = State()
    vacancy_detail = State()
    cv = State()
