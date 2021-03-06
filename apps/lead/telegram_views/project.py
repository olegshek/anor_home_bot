from aiogram.types import ContentType

from apps.bot import dispatcher as dp, bot, keyboards, messages
from apps.bot.messages import get_message
from apps.bot.tortoise_models import Button
from apps.bot.utils import try_delete_message
from apps.lead import callback_filters
from apps.lead.states import LeadForm
from apps.lead.tortoise_models import CommercialProject, ResidentialProject, Apartment, Store, ApartmentTransaction, \
    StoreTransaction
from apps.lead.tortoise_models.lead import DuplexTransaction
from apps.lead.tortoise_models.project import Duplex
from core.callback_filters import message_is_digit


def get_project_message(project, locale):
    project_description = getattr(project, f'description_{locale}')
    return f'<b>{project.name}</b>\n\n' \
           f'{project_description}'


async def send_project_choice(user_id, message_id, locale, project_type):
    project_model = CommercialProject if project_type == 'commercial' else ResidentialProject
    projects = await project_model.all().order_by('name')

    if projects:
        await try_delete_message(user_id, message_id)

        menu_keyboard = await keyboards.cart(locale)
        menu_message = await get_message('residence_choice', locale)
        await bot.send_message(user_id, menu_message, reply_markup=menu_keyboard)

        for project in projects:
            keyboard = await keyboards.project_choice(project, locale)
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

    message_code = 'room_quantity' if project_type == 'residential' else 'floor_number'
    message = await get_message(message_code, locale)
    keyboard = await keyboards.room_quantity_or_floor_number_choice(project_id, project_type, locale)

    await LeadForm.room_quantity_or_floor_number_choice.set()
    await bot.send_message(user_id, message, reply_markup=keyboard)


async def send_project_object(user_id, message_id, locale, state, object_id=None, option=None):
    async with state.proxy() as data:
        room_quantity_or_floor_number = data['room_quantity_or_floor_number']
        project_id = data['project_id']
        project_type = data['project_type']

    object_model = Apartment if project_type == 'residential' else Store
    number_field_name = 'room_quantity' if project_type == 'residential' else 'floor_number'

    transaction_model = ApartmentTransaction if project_type == 'residential' else StoreTransaction
    transaction__object_field_name = 'apartment_id' if project_type == 'residential' else 'store_id'

    added_objects = await transaction_model.filter(lead_id__isnull=True, customer_id=user_id).values_list(
        transaction__object_field_name,
        flat=True
    )

    project_objects = object_model.filter(
        project__id=project_id,
        **{number_field_name: room_quantity_or_floor_number}
    ).order_by('id')

    if object_model == Apartment:
        project_objects = project_objects.exclude(duplex_id__isnull=False)

    project_object = await project_objects.first()

    if object_id and option:
        current_object = await object_model.filter(id=object_id).first()

        if current_object:
            exclude_data = {'id': object_id}

            if object_model == ApartmentTransaction:
                exclude_data['duplex_id__isnull'] = False

            project_objects_cor = object_model.filter(
                project__id=project_id,
                **{
                    number_field_name: room_quantity_or_floor_number,
                    f'id__{option}': current_object.id
                }
            ).exclude(**exclude_data).order_by('id')

            if option == 'gte':
                project_object = await project_objects_cor.first()
            else:
                objects = (await project_objects_cor)
                project_object = objects[-1] if objects else None

    if not project_object:
        return

    project_ids = await project_objects.values_list('id', flat=True)
    project_number = project_ids.index(project_object.id) + 1
    projects_quantity = len(project_ids)
    message = f'<b>{await messages.get_message("square", locale)} {project_object.square} ??2</b>\n\n' \
              f'{getattr(project_object, f"description_{locale}")}'
    keyboard = await keyboards.project_object_menu(project_object.id, locale, added_objects, projects_quantity,
                                                   project_number)
    photo = await project_object.photo

    await try_delete_message(user_id, message_id)

    await bot.send_message(user_id, '??????', reply_markup=await keyboards.cart(locale))
    await LeadForm.project_object_choice.set()

    if photo:
        with open(photo.get_path(), 'rb') as photo_file:
            return await bot.send_photo(user_id, photo_file, caption=message, reply_markup=keyboard, parse_mode='HTML')

    await bot.send_message(user_id, message, reply_markup=keyboard, parse_mode='HTML')


async def send_duplex(user_id, message_id, project_id, locale, duplex_id=None, lookups=None, apartment_id=None,
                      floor_number_filter=None):
    duplex = await Duplex.filter(project_id=project_id).order_by('room_quantity').first()

    if duplex_id and lookups:
        current_duplex = await Duplex.get(id=duplex_id)
        duplex = await Duplex.filter(
            project_id=project_id,
            **{f'room_quantity__{lookups}': current_duplex.room_quantity}
        ).exclude(id=current_duplex.id).order_by('room_quantity').first()

    if not duplex:
        return

    apartment = await duplex.apartments.order_by('floor_number').first()

    if apartment_id and floor_number_filter:
        current_apartment = await Apartment.get(id=apartment_id)
        duplex = await current_apartment.duplex
        apartment = await duplex.apartments.filter(
            **{floor_number_filter: current_apartment.floor_number}
        ).exclude(id=current_apartment.id).first()

    if not apartment:
        return

    added_duplexes = await DuplexTransaction.filter(lead_id__isnull=True, customer_id=user_id).values_list('duplex_id',
                                                                                                           flat=True)

    duplex_ids = list(await Duplex.filter(project_id=project_id).order_by('room_quantity').values_list('id', flat=True))
    duplex_number = duplex_ids.index(duplex.id) + 1
    duplexes_quantity = len(duplex_ids)

    message = f'<b>{await messages.get_message("square", locale)}</b> {apartment.square} ??2\n\n' \
              f'{getattr(apartment, f"description_{locale}")}'
    keyboard = await keyboards.project_object_menu(apartment.id, locale, added_duplexes, duplexes_quantity,
                                                   duplex_number, True, apartment.floor_number)
    photo = await apartment.photo

    await try_delete_message(user_id, message_id)
    await bot.send_message(user_id, '??????', reply_markup=await keyboards.cart(locale))
    await LeadForm.project_object_choice.set()

    if photo:
        with open(photo.get_path(), 'rb') as photo_file:
            return await bot.send_photo(user_id, photo_file, caption=message, reply_markup=keyboard, parse_mode='HTML')

    await bot.send_message(user_id, message, reply_markup=keyboard, parse_mode='HTML')


@dp.message_handler(callback_filters.project_type, state=LeadForm.project_type.state, content_types=[ContentType.TEXT])
async def choose_project_type(message, locale, state):
    project_type_text = message.text
    project_type = (await Button.filter(**{f'text_{locale}': project_type_text}).first()).code

    async with state.proxy() as data:
        data['project_type'] = project_type

    await send_project_choice(message.from_user.id, message.message_id, locale, project_type)


@dp.callback_query_handler(callback_filters.choose_button, state=LeadForm.project_choice.state)
async def project_choice(query, state, locale):
    user_id = query.from_user.id
    project_id = int(query.data.split(':')[1])

    async with state.proxy() as data:
        data['project_id'] = project_id
        project_type = data['project_type']

    await send_project_menu(user_id, query.message.message_id, locale, project_type, project_id)


@dp.message_handler(callback_filters.project_menu, state=LeadForm.project_menu.state, content_types=[ContentType.TEXT])
async def process_project_menu(message, state, locale):
    user_id = message.from_user.id
    code = (await Button.filter(**{f'text_{locale}': message.text}).first()).code
    message_id = message.message_id

    async with state.proxy() as data:
        project_id = data['project_id']
        project_type = data['project_type']

    project_model = ResidentialProject if project_type == 'residential' else CommercialProject
    project = await project_model.get(id=project_id)

    if code in ['apartment_choice', 'store_choice']:
        await send_room_quantity_or_floor_number(user_id, message_id, locale, project_id, project_type)

    if code == 'about_project':
        photos = await project.photos.all()
        documents = await project.documents.all()
        location = await project.location

        await try_delete_message(user_id, message_id)

        about_project = getattr(project, f'about_{locale}')

        for photo in photos:
            with open(photo.get_path(), 'rb') as photo_data:
                await bot.send_photo(
                    user_id,
                    photo_data,
                    caption=about_project,
                    parse_mode='HTML',
                    reply_markup=await keyboards.back_keyboard(locale)
                )

        for document in documents:
            with open(document.get_path(), 'rb') as document_data:
                await bot.send_document(
                    user_id,
                    document_data,
                    caption=getattr(document, f'description_{locale}'),
                    parse_mode='HTML',
                    reply_markup=await keyboards.back_keyboard(locale)
                )

        if location and location.latitude and location.longitude:
            location_message = await bot.send_location(user_id, location.latitude, location.longitude)
            await bot.send_message(
                user_id,
                getattr(location, f'description_{locale}'),
                reply_to_message_id=location_message.message_id,
                reply_markup=await keyboards.back_keyboard(locale)
            )

        await LeadForm.about_project.set()

    if code == 'download_catalogue':
        await try_delete_message(user_id, message_id)

        documents = await project.catalogue_documents.all()

        for document in documents:
            with open(document.get_path(), 'rb') as document_data:
                await bot.send_document(
                    user_id,
                    document_data,
                    caption=getattr(document, f'description_{locale}'),
                    parse_mode='HTML',
                    reply_markup=await keyboards.back_keyboard(locale)
                )

        await LeadForm.catalogue.set()


@dp.message_handler(message_is_digit, state=LeadForm.room_quantity_or_floor_number_choice.state,
                    content_types=[ContentType.TEXT])
async def room_quantity_or_floor_number_choice(message, state, locale):
    user_id = message.from_user.id
    room_quantity_or_floor_number = int(message.text)

    async with state.proxy() as data:
        data['room_quantity_or_floor_number'] = room_quantity_or_floor_number

    await send_project_object(user_id, message.message_id, locale, state)


@dp.callback_query_handler(callback_filters.is_switch, state=LeadForm.project_object_choice.state)
async def switch_project_object(query, state, locale):
    user_id = query.from_user.id
    data = query.data.split(';')
    object_id = int(data[0])
    lookups = data[1]

    async with state.proxy() as data:
        project_id = data['project_id']
        project_type = data['project_type']

    if project_type == 'residential':
        apartment = await Apartment.get(id=object_id)
        duplex = await apartment.duplex

        if duplex:
            return await send_duplex(user_id, query.message.message_id, project_id, locale, duplex.id, lookups)

    await send_project_object(user_id, query.message.message_id, locale, state, object_id, lookups)


@dp.callback_query_handler(callback_filters.is_duplex, state=LeadForm.room_quantity_or_floor_number_choice.state)
async def select_duplex(query, locale, state):
    user_id = query.from_user.id

    async with state.proxy() as data:
        project_id = data['project_id']
        data['duplex_choice'] = True

    await send_duplex(user_id, query.message.message_id, project_id, locale)


@dp.callback_query_handler(callback_filters.is_floor_number_switch, state=LeadForm.project_object_choice.state)
async def switch_duplex_floor_number(query, state, locale):
    user_id = query.from_user.id
    data = query.data.split(';')
    apartment_id = int(data[0])
    filter_name = data[1]

    async with state.proxy() as data:
        project_id = data['project_id']

    await send_duplex(user_id, query.message.message_id, project_id, locale, apartment_id=apartment_id,
                      floor_number_filter=filter_name)
