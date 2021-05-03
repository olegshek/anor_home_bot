from aiogram import types

from apps.bot import dispatcher as dp, bot, keyboards, messages
from apps.bot.telegram_views import send_main_menu
from apps.bot.tortoise_models import Button
from apps.bot.utils import try_delete_message
from apps.lead import callback_filters
from apps.lead.states import LeadForm
from apps.lead.telegram_views.project import send_project_object, send_project_choice, send_duplex, send_project_menu
from apps.lead.tortoise_models import ApartmentTransaction, StoreTransaction, Lead, Customer, Apartment
from apps.lead.tortoise_models.lead import DuplexTransaction


async def remove_all_transactions(user_id):
    await ApartmentTransaction.filter(customer_id=user_id, lead_id__isnull=True).delete()
    await StoreTransaction.filter(customer_id=user_id, lead_id__isnull=True).delete()


async def send_cart_menu(user_id, message_id, locale, state, transaction_id=None, option=None):
    async with state.proxy() as data:
        project_type = data['project_type']
        duplex_cart = data.get('duplex_cart', None)

    transaction_model = ApartmentTransaction if project_type == 'residential' else StoreTransaction

    transaction = await transaction_model.filter(
        customer_id=user_id,
        lead_id__isnull=True
    ).order_by('created_at').first()

    if transaction_id and option:
        transaction_model = DuplexTransaction if duplex_cart else transaction_model
        current_object = await transaction_model.filter(id=transaction_id).first()

        if current_object:
            transaction = await transaction_model.filter(
                customer_id=user_id,
                lead_id__isnull=True,
                **{f'created_at__{option}': current_object.created_at}
            ).exclude(id=transaction_id).order_by('created_at').first()

            if not transaction and project_type == 'residential' and (
                    (transaction_model == DuplexTransaction and option == 'lte') or
                    (transaction_model == ApartmentTransaction and option == 'gte') or
                    not option
            ):
                transaction_model = ApartmentTransaction if transaction_model == DuplexTransaction else \
                    DuplexTransaction
                ordering_lookup = '-created_at' if transaction_model == ApartmentTransaction else 'created_at'

                transaction = await transaction_model.filter(
                    customer_id=user_id,
                    lead_id__isnull=True
                ).order_by(ordering_lookup).first()

                if not transaction:
                    return

    if not transaction:
        if project_type == 'residential':
            transaction_model = DuplexTransaction
            transaction = await transaction_model.filter(customer_id=user_id, lead_id__isnull=True).order_by(
                'created_at').first()

    async with state.proxy() as data:
        data['duplex_cart'] = True if transaction_model == DuplexTransaction else False

    if not transaction:
        await try_delete_message(user_id, message_id)
        await bot.send_message(user_id, await messages.get_message('empty_cart', locale))

        state_name = await state.get_state()

        if state_name == LeadForm.project_object_choice.state:
            return await send_project_object(user_id, message_id, locale, state)

        if state_name in [LeadForm.cart.state, LeadForm.project_choice.state]:
            return await send_project_choice(user_id, message_id, locale, project_type)

        if state_name == LeadForm.project_menu.state:
            async with state.proxy() as data:
                project_id = data['project_id']

            return await send_project_menu(user_id, message_id, locale, project_type, project_id)

        return

    transactions = list(
        await transaction_model.filter(customer_id=user_id, lead_id__isnull=True).order_by('created_at')
    )

    if transaction_model == ApartmentTransaction:
        transactions += list(
            await DuplexTransaction.filter(customer_id=user_id, lead_id__isnull=True).order_by('created_at')
        )

    if transaction_model == DuplexTransaction:
        apartment_transactions = list(
            await ApartmentTransaction.filter(customer_id=user_id, lead_id__isnull=True).order_by('created_at')
        )
        transactions = apartment_transactions + transactions

    transaction_number = transactions.index(transaction) + 1
    transactions_quantity = len(transactions)

    project_model = 'apartment' if transaction_model == ApartmentTransaction else \
        'store' if transaction_model == StoreTransaction else 'duplex'

    project_object = await getattr(transaction, project_model)
    project = await project_object.project

    message = f'<b>{project.name}\n'

    if project_type != 'commercial':
        room_quantity_message = await messages.get_message('room_quantity_info', locale)
        message += f'{room_quantity_message} {project_object.room_quantity}\n'
    else:
        floor_number_message = await messages.get_message('floor_number_message', locale)
        message += f'{floor_number_message} {project_object.floor_number}\n'

    if transaction_model == DuplexTransaction:
        duplex_name = getattr(await Button.get(code='duplex'), f'text_{locale}')
        message += f'{duplex_name}</b>\n\n'
    else:
        message += f'{project_object.square}m</b>\n\n'

    if transaction_model != DuplexTransaction:
        message += f'{getattr(project_object, f"description_{locale}")}'

    keyboard = await keyboards.cart_menu(transaction.id, locale, transactions_quantity, transaction_number)

    reply_to_message_id = None
    await try_delete_message(user_id, message_id)

    if transaction_model != DuplexTransaction:
        photos = await project_object.photos
        media_group = types.MediaGroup()

        for photo in photos:
            media_group.attach_photo(types.InputFile(photo.get_path()))

        sent_group = await bot.send_media_group(user_id, media_group)
        reply_to_message_id = sent_group[0].message_id

    await LeadForm.cart.set()
    await bot.send_message(user_id, message, reply_markup=keyboard, reply_to_message_id=reply_to_message_id,
                           parse_mode='HTML')


@dp.callback_query_handler(callback_filters.add_to_cart, state=LeadForm.project_object_choice.state)
async def add_to_cart(query, locale, state):
    user_id = query.from_user.id
    object_id = int(query.data.split(';')[1])
    message_id = query.message.message_id

    async with state.proxy() as data:
        project_type = data['project_type']
        project_id = data['project_id']

    transaction_model = ApartmentTransaction if project_type == 'residential' else StoreTransaction
    object_field_name = 'apartment_id' if project_type == 'residential' else 'store_id'

    duplex = None

    if project_type == 'residential':
        apartment = await Apartment.get(id=object_id)
        duplex = await apartment.duplex

        if duplex:
            transaction_model = DuplexTransaction
            object_field_name = 'duplex_id'
            object_id = duplex.id

    await transaction_model.create(customer_id=user_id, **{object_field_name: object_id})

    if duplex:
        return await send_duplex(user_id, message_id, project_id, locale)

    await send_project_object(user_id, message_id, locale, state, object_id)


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
        duplex_cart = data.get('duplex_cart', None)

    transaction_model = ApartmentTransaction if project_type == 'residential' else StoreTransaction

    if 'remove_from_cart' in query_data:
        if duplex_cart:
            transaction_model = DuplexTransaction

        transaction_id = int(query_data[1])
        await transaction_model.filter(id=transaction_id).delete()
        return await send_cart_menu(user_id, query.message.message_id, locale, state)

    if 'continue_review' in query.data:
        async with state.proxy() as data:
            data['duplex_cart'] = False

        return await send_project_choice(user_id, message_id, locale, project_type)

    if 'consultation_request' in query.data:
        transactions = list(await transaction_model.filter(customer_id=user_id, lead_id__isnull=True))
        duplex_transactions = []

        if project_type == 'residential':
            duplex_transactions = list(await DuplexTransaction.filter(customer_id=user_id, lead_id__isnull=True))

        message = ''

        for count, transaction in enumerate(transactions + duplex_transactions):
            transaction_model = transaction.__class__
            project_model = 'apartment' if transaction_model == ApartmentTransaction else \
                'store' if transaction_model == StoreTransaction else 'duplex'
            project_object = await getattr(transaction, project_model)
            project = await project_object.project

            message += f'<b>{count + 1}. {project.name}\n'

            if project_type != 'commercial':
                room_quantity_message = await messages.get_message('room_quantity_info', locale)
                message += f'{room_quantity_message} {project_object.room_quantity}\n'
            else:
                floor_number_message = await messages.get_message('floor_number_message', locale)
                message += f'{floor_number_message} {project_object.floor_number}\n'

            if transaction_model == DuplexTransaction:
                duplex_name = getattr(await Button.get(code='duplex'), f'text_{locale}')
                message += f'{duplex_name}</b>\n\n'
            else:
                message += f'{project_object.square}m</b>\n\n'

        keyboard = await keyboards.confirmation(locale)

        async with state.proxy() as data:
            data['duplex_cart'] = False

        await LeadForm.lead_confirmation.set()
        await try_delete_message(user_id, message_id)
        await bot.send_message(user_id, message, reply_markup=keyboard, parse_mode='HTML')


@dp.callback_query_handler(callback_filters.confirm_button, state=LeadForm.lead_confirmation.state)
async def confirm_lead(query, locale, state):
    user_id = query.from_user.id

    async with state.proxy() as data:
        project_type = data['project_type']

    transaction_model = ApartmentTransaction if project_type == 'residential' else StoreTransaction

    lead = await Lead.create(customer_id=user_id)
    await transaction_model.filter(customer_id=user_id, lead_id__isnull=True).update(lead_id=lead.id)

    if project_type == 'residential':
        await DuplexTransaction.filter(customer_id=user_id, lead_id__isnull=True).update(lead_id=lead.id)

    message = await messages.get_message('request_accepted', locale)
    await bot.edit_message_text(message, user_id, query.message.message_id)
    message = await messages.get_message('request_number', locale) + f' {lead.number}'
    await bot.send_message(user_id, message, reply_markup=keyboards.remove_keyboard)

    customer = await Customer.get(id=user_id)
    await send_main_menu(customer, locale, state)
