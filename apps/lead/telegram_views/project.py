from aiogram import types

from apps.bot import dispatcher as dp, bot, keyboards
from apps.bot.messages import get_message
from apps.bot.utils import try_delete_message
from apps.lead import callback_filters
from apps.lead.states import LeadForm
from apps.lead.tortoise_models import CommercialProject, ResidentialProject, Apartment, Store
from core.callback_filters import is_digit


def get_project_message(project, locale):
    project_description = getattr(project, f'description_{locale}')
    return f'<b>{project.name}</b>\n\n' \
           f'{project_description}'


async def send_project_choice(user_id, message_id, locale, project_type):
    await try_delete_message(user_id, message_id)

    project_model = CommercialProject if project_type == 'commercial' else ResidentialProject
    projects = await project_model.all().order_by(f'name')
    projects_len = len(projects)

    for project in projects:
        is_last = True if projects.index(project) == projects_len - 1 else False
        keyboard = await keyboards.project_choice(project_type, project, locale, is_last)
        photo = await project.main_photo
        text = get_project_message(project, locale)

        with open(photo.get_path(), 'rb') as photo_data:
            await bot.send_photo(
                user_id,
                photo_data,
                caption=text,
                reply_markup=keyboard,
                parse_mode='HTML'
            )

    await LeadForm.project_choice.set()


async def send_project_menu(user_id, message_id, locale, project_type, project_id):
    await try_delete_message(user_id, message_id)

    project_model = CommercialProject if project_type == 'commercial' else ResidentialProject
    project = await project_model.get(id=project_id)
    text = get_project_message(project, locale)
    photo = await project.main_photo
    keyboard = await keyboards.project_menu(project_type, locale)

    await LeadForm.project_menu.set()

    with open(photo.get_path(), 'rb') as photo_data:
        await bot.send_photo(
            user_id,
            photo_data,
            caption=text,
            reply_markup=keyboard,
            parse_mode='HTML'
        )


async def send_room_quantity_or_floor_number(user_id, message_id, locale, project_id, project_type):
    await try_delete_message(user_id, message_id)

    message_code = 'room_quantity' if project_type == 'commercial' else 'floor_number'
    message = await get_message(message_code, locale)
    keyboard = await keyboards.room_quantity_or_floor_number_choice(project_id, project_type, locale)

    await LeadForm.room_quantity_or_floor_number_choice.set()
    await bot.send_message(user_id, message, reply_markup=keyboard)


async def send_project_object(user_id, message_id, locale, state, object_id=None, option=None):
    async with state.proxy() as data:
        room_quantity_or_floor_number = data['room_quantity_or_floor_number']
        project_id = data['project_id']
        project_type = data['project_type']
        added_objects = data.get('apartments', []) if project_type == 'residential' else data.get('stores', [])

    object_model = Apartment if project_type == 'residential' else Store
    number_field_name = 'room_quantity' if project_type == 'residential' else 'floor_number'

    project_object = await object_model.filter(
        project__id=project_id,
        **{number_field_name: room_quantity_or_floor_number}
    ).order_by('square').first()

    if object_id and option:
        current_object = await object_model.filter(id=object_id).first()

        if current_object:
            project_object = await object_model.filter(
                project__id=project_id,
                **{
                    number_field_name: room_quantity_or_floor_number,
                    f'square__{option}': current_object.square
                }
            ).exclude(id=object_id).order_by('square').first()

    if not project_object:
        return

    message = f'<b>{project_object.square}m</b>\n\n' \
              f'{getattr(project_object, f"description_{locale}")}'
    keyboard = await keyboards.project_object_menu(project_object.id, locale, added_objects)
    photos = await project_object.photos
    media_group = types.MediaGroup()

    for photo in photos:
        media_group.attach_photo(types.InputFile(photo.get_path()))

    await try_delete_message(user_id, message_id)

    sent_group = await bot.send_media_group(user_id, media_group)

    await LeadForm.project_object_choice.set()
    await bot.send_message(user_id, message, reply_markup=keyboard, reply_to_message_id=sent_group[0].message_id,
                           parse_mode='HTML')


@dp.callback_query_handler(callback_filters.project_type, state=LeadForm.project_type.state)
async def choose_project_type(query, locale, state):
    project_type = query.data

    async with state.proxy() as data:
        data['project_type'] = project_type

    await send_project_choice(query.from_user.id, query.message.message_id, locale, project_type)


@dp.callback_query_handler(callback_filters.residence_choice, state=LeadForm.project_choice.state)
async def residence_choice(query, state, locale):
    user_id = query.from_user.id
    project_id = int(query.data.split(':')[1])

    async with state.proxy() as data:
        data['project_id'] = project_id
        project_type = data['project_type']

    await send_project_menu(user_id, query.message.message_id, locale, project_type, project_id)


@dp.callback_query_handler(callback_filters.project_menu, state=LeadForm.project_menu.state)
async def process_project_menu(query, state, locale):
    user_id = query.from_user.id
    code = query.data
    message_id = query.message.message_id

    async with state.proxy() as data:
        project_id = data['project_id']
        project_type = data['project_type']

    if code in ['apartment_choice', 'store_choice']:
        await send_room_quantity_or_floor_number(user_id, message_id, locale, project_id, project_type)


@dp.callback_query_handler(is_digit, state=LeadForm.room_quantity_or_floor_number_choice.state)
async def room_quantity_or_floor_number_choice(query, state, locale):
    user_id = query.from_user.id
    room_quantity_or_floor_number = int(query.data)

    async with state.proxy() as data:
        data['room_quantity_or_floor_number'] = room_quantity_or_floor_number

    await send_project_object(user_id, query.message.message_id, locale, state)


@dp.callback_query_handler(callback_filters.is_switch, state=LeadForm.project_object_choice.state)
async def switch_project_object(query, state, locale):
    user_id = query.from_user.id
    data = query.data.split(';')
    object_id = int(data[0])
    lookups = data[1]

    await send_project_object(user_id, query.message.message_id, locale, state, object_id, lookups)



