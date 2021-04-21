from apps.bot.tortoise_models import Button, KeyboardButtonsOrdering
from apps.lead.tortoise_models import ResidentialProject, CommercialProject
from core.filters import callback_filter


async def language_choice(message):
    en_text = (await Button.get(code='en')).text_en
    ru_text = (await Button.get(code='ru')).text_ru
    uz_text = (await Button.get(code='uz')).text_uz
    return message.text in [en_text, ru_text, uz_text]


async def project_type(query):
    return query.data in ['residential', 'commercial']


async def residence_choice(query):
    data = query.data
    data = data.split(':')
    project_variant = 'residential' if 'residential' in data else 'commercial' if 'commercial' in data else False

    if not project_variant:
        return False

    project_model = ResidentialProject if project_variant == 'residential' else CommercialProject
    projects_ids = await project_model.all().values_list('id', flat=True)

    return len(data) > 1 and int(data[1]) in projects_ids


async def project_menu(query):
    return await callback_filter(query, 'residential_project_menu') or \
           await callback_filter(query, 'commercial_project_menu')


def is_switch(query):
    data = query.data.split(';')
    return len(data) == 2 and data[1] in ['gte', 'lte']


def add_to_cart(query):
    return 'add_to_cart' in query.data


def cart(query):
    return query.data == 'cart'


def cart_menu(query):
    code = query.data.split(';')[0]
    return code in ['remove_from_cart', 'consultation_request', 'continue_review']
