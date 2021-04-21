from aiogram import types

from apps.bot import dispatcher as dp, bot, keyboards, messages
from apps.bot.utils import try_delete_message
from apps.lead import callback_filters
from apps.lead.states import LeadForm
from apps.lead.telegram_views.project import send_project_object, send_project_choice
from apps.lead.tortoise_models import ApartmentTransaction, StoreTransaction


async def remove_all_transactions(user_id):
    await ApartmentTransaction.filter(customer_id=user_id, lead_id__isnull=True).delete()
    await StoreTransaction.filter(customer_id=user_id, lead_id__isnull=True).delete()


async def send_cart_menu(user_id, message_id, locale, state, transaction_id=None, option=None):
    async with state.proxy() as data:
        project_type = data['project_type']

    transaction_model = ApartmentTransaction if project_type == 'residential' else StoreTransaction

    transaction = await transaction_model.filter(
        customer_id=user_id,
        lead_id__isnull=True
    ).order_by('created_at').first()

    if transaction_id and option:
        current_object = await transaction_model.filter(id=transaction_id).first()

        if current_object:
            transaction = await transaction_model.filter(
                customer_id=user_id,
                lead_id__isnull=True,
                **{f'created_at__{option}': current_object.created_at}
            ).exclude(id=transaction_id).order_by('created_at').first()

    if not transaction:
        await bot.send_message(user_id, await messages.get_message('empty_cart', locale))

        state_name = await state.get_state()

        if state_name == LeadForm.project_object_choice.state:
            return await send_project_object(user_id, message_id, locale, state)

        if state_name == LeadForm.cart.state:
            return await send_project_choice(user_id, message_id, locale, project_type)

    transaction_ids = list(
        await transaction_model.filter(customer_id=user_id).order_by('created_at').values_list('id', flat=True)
    )
    transaction_number = transaction_ids.index(transaction.id) + 1
    transactions_quantity = len(transaction_ids)

    project_model = 'apartment' if project_type == 'residential' else 'store'
    project_object = await getattr(transaction, project_model)
    project = await project_object.project

    room_quantity_message = await messages.get_message('room_quantity_info', locale)

    message = f'<b>{project.name}\n' \
              f'{room_quantity_message} {project_object.room_quantity}\n' \
              f'{project_object.square}m</b>\n\n' \
              f'{getattr(project_object, f"description_{locale}")}'
    keyboard = await keyboards.cart_menu(transaction.id, locale, transactions_quantity, transaction_number)

    photos = await project_object.photos
    media_group = types.MediaGroup()

    for photo in photos:
        media_group.attach_photo(types.InputFile(photo.get_path()))

    await try_delete_message(user_id, message_id)

    sent_group = await bot.send_media_group(user_id, media_group)

    await LeadForm.cart.set()
    await bot.send_message(user_id, message, reply_markup=keyboard, reply_to_message_id=sent_group[0].message_id,
                           parse_mode='HTML')


@dp.callback_query_handler(callback_filters.add_to_cart, state=LeadForm.project_object_choice.state)
async def add_to_cart(query, locale, state):
    user_id = query.from_user.id
    object_id = int(query.data.split(';')[1])

    async with state.proxy() as data:
        project_type = data['project_type']

    transaction_model = ApartmentTransaction if project_type == 'residential' else StoreTransaction
    object_field_name = 'apartment_id' if project_type == 'residential' else 'store_id'
    await transaction_model.create(customer_id=user_id, **{object_field_name: object_id})

    await send_project_object(user_id, query.message.message_id, locale, state, object_id)


@dp.callback_query_handler(callback_filters.cart, state='*')
async def cart(query, locale, state):
    user_id = query.from_user.id
    await send_cart_menu(user_id, query.message.message_id, locale, state)


@dp.callback_query_handler(callback_filters.is_switch, state=LeadForm.cart.state)
async def switch_cart(query, locale, state):
    user_id = query.from_user.id
    data = query.data.split(';')
    transaction_id = int(data[0])
    lookups = data[1]
    await send_cart_menu(user_id, query.message.message_id, locale, state, transaction_id, lookups)


@dp.callback_query_handler(callback_filters.cart_menu, state=LeadForm.cart.state)
async def process_cart_menu(query, locale, state):
    user_id = query.from_user.id
    message_id = query.message.message_id
    query_data = query.data.split(';')

    async with state.proxy() as data:
        project_type = data['project_type']

    transaction_model = ApartmentTransaction if project_type == 'residential' else StoreTransaction

    if 'remove_from_cart' in query_data:
        transaction_id = query_data[1]
        await transaction_model.filter(id=transaction_id).delete()
        return await send_cart_menu(user_id, query.message.message_id, locale, state)

    if 'continue_review' in query.data:
        return await send_project_choice(user_id, message_id, locale, project_type)

    if 'consultation_request' in query.data:
        transactions = await transaction_model.filter(customer_id=user_id, lead_id__isnull=True)
