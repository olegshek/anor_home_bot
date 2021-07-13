from aiogram.types import ContentType
from django.conf import settings

from apps.bot import dispatcher as dp, bot, keyboards, messages
from apps.bot.telegram_views import send_main_menu
from apps.bot.tortoise_models import Button
from apps.bot.utils import try_delete_message
from apps.company import callback_filters
from apps.company.states import CompanyForm
from apps.company.tortoise_models import CompanyText, CompanyPhoto, CompanyDocument, Service, Vacancy, ServiceRequest, \
    VacancyRequest
from apps.lead.callback_filters import choose_button
from apps.lead.tortoise_models import Customer


@dp.message_handler(callback_filters.anorhome_menu, state=CompanyForm.menu.state, content_types=[ContentType.TEXT])
async def anorhome_menu(message, locale, state):
    user_id = message.from_user.id
    message_id = message.message_id
    code = (await Button.filter(**{f'text_{locale}': message.text}).first()).code

    if code == 'about_company':
        await try_delete_message(user_id, message_id)
        company_text = await CompanyText.first()
        company_photos = await CompanyPhoto.all()
        company_documents = await CompanyDocument.all()

        for company_photo in company_photos:
            photo = await company_photo.photo
            with open(photo.get_path(), 'rb') as photo_data:
                await bot.send_photo(
                    user_id,
                    photo_data,
                    parse_mode='HTML'
                )

        await bot.send_message(user_id, getattr(company_text, f'text_{locale}'),
                               reply_markup=await keyboards.back_keyboard(locale))

        for company_document in company_documents:
            photo = await company_document.document
            with open(photo.get_path(), 'rb') as document_data:
                await bot.send_photo(
                    user_id,
                    document_data,
                    caption=getattr(photo, f'description_{locale}'),
                    parse_mode='HTML'
                )

        await CompanyForm.about.set()

    if code == 'corporate_customer':
        services = await Service.all()
        services_len = len(services)
        await bot.send_message(user_id, '✔️', reply_markup=await keyboards.back_keyboard(locale))

        for service in services:
            is_last = True if services.index(service) == services_len - 1 else False
            photo = await service.photo
            keyboard = await keyboards.services_or_vacancies(service, locale, is_last)

            with open(photo.get_path(), 'rb') as photo_data:
                await bot.send_photo(
                    user_id,
                    photo_data,
                    caption=getattr(service, f'name_{locale}'),
                    parse_mode='HTML',
                    reply_markup=keyboard
                )

        await CompanyForm.services.set()

    if code == 'vacancies':
        vacancies = await Vacancy.all()
        vacancies_len = len(vacancies)

        for vacancy in vacancies:
            is_last = True if vacancies.index(vacancy) == vacancies_len - 1 else False
            photo = await vacancy.photo
            keyboard = await keyboards.services_or_vacancies(vacancy, locale, is_last)

            await bot.send_message(user_id, '✔️', reply_markup=await keyboards.back_keyboard(locale))

            with open(photo.get_path(), 'rb') as photo_data:
                await bot.send_photo(
                    user_id,
                    photo_data,
                    caption=getattr(vacancy, f'name_{locale}'),
                    parse_mode='HTML',
                    reply_markup=keyboard
                )

        await CompanyForm.vacancies.set()


@dp.callback_query_handler(choose_button, state=CompanyForm.services.state)
async def choose_service(query, locale, state):
    user_id = query.from_user.id
    message_id = query.message.message_id
    service_id = int(query.data.split(':')[1])

    await try_delete_message(user_id, message_id)

    service = await Service.filter(id=service_id).first()

    if service:
        async with state.proxy() as data:
            data['service_id'] = service_id

        name = getattr(service, f'name_{locale}')
        description = getattr(service, f'description_{locale}')
        photo = await service.photo
        keyboard = await keyboards.apply(locale)
        message = f'<b>{name}</b>\n\n' \
                  f'{description}'

        with open(photo.get_path(), 'rb') as photo_data:
            await bot.send_photo(
                user_id,
                photo_data,
                caption=message,
                parse_mode='HTML',
                reply_markup=keyboard
            )

        await CompanyForm.service_detail.set()


@dp.callback_query_handler(choose_button, state=CompanyForm.vacancies.state)
async def choose_vacancy(query, locale, state):
    user_id = query.from_user.id
    message_id = query.message.message_id
    vacancy_id = int(query.data.split(':')[1])

    await try_delete_message(user_id, message_id)

    vacancy = await Vacancy.filter(id=vacancy_id).first()

    if vacancy:
        async with state.proxy() as data:
            data['vacancy_id'] = vacancy_id

        name = getattr(vacancy, f'name_{locale}')
        description = getattr(vacancy, f'description_{locale}')
        photo = await vacancy.photo
        keyboard = await keyboards.apply(locale)
        message = f'<b>{name}</b>\n\n' \
                  f'{description}'

        with open(photo.get_path(), 'rb') as photo_data:
            await bot.send_photo(
                user_id,
                photo_data,
                caption=message,
                parse_mode='HTML',
                reply_markup=keyboard
            )

        await CompanyForm.vacancy_detail.set()


@dp.message_handler(callback_filters.is_apply, state=CompanyForm.service_detail.state, content_types=[ContentType.TEXT])
async def apply_service(message, locale, state):
    user_id = message.from_user.id

    async with state.proxy() as data:
        service_id = data['service_id']

    request = await ServiceRequest.create(customer_id=user_id, service_id=service_id)

    await try_delete_message(user_id, message.message_id)
    message = await messages.get_message('request_accepted', locale)
    await bot.send_message(user_id, message)
    message = await messages.get_message('request_number', locale) + f' {request.number}'
    await bot.send_message(user_id, message, reply_markup=keyboards.remove_keyboard)

    customer = await Customer.get(id=user_id)
    await send_main_menu(customer, locale, state)


@dp.message_handler(callback_filters.is_apply, state=CompanyForm.vacancy_detail.state, content_types=[ContentType.TEXT])
async def apply_vacancy(message, locale, state):
    user_id = message.from_user.id
    message_id = message.message_id

    await try_delete_message(user_id, message.message_id)
    message = await messages.get_message('cv', locale)
    keyboard = await keyboards.back_keyboard(locale)

    await CompanyForm.cv.set()

    await try_delete_message(user_id, message_id)
    await bot.send_message(user_id, message, reply_markup=keyboard)


@dp.message_handler(content_types=[ContentType.DOCUMENT], state=CompanyForm.cv.state)
async def apply_cv(message, locale, state):
    user_id = message.from_user.id
    file_id = message.document.file_id

    async with state.proxy() as data:
        vacancy_id = data['vacancy_id']

    request = await VacancyRequest.create(customer_id=user_id, vacancy_id=vacancy_id, cv_file_id=file_id)

    message = await messages.get_message('request_accepted', locale)
    await bot.send_message(user_id, message, reply_markup=keyboards.remove_keyboard)
    message = await messages.get_message('request_number', locale) + f' {request.number}'
    await bot.send_message(user_id, message)

    customer = await Customer.get(id=user_id)

    vacancy = await request.vacancy
    hiring_message = f'{customer.full_name}\n' \
                     f'{customer.phone_number}\n\n' \
                     f'Вакансия: {vacancy.name_ru}'
    await bot.send_document(settings.HIRING_CHANNEL, file_id, caption=hiring_message)

    await send_main_menu(customer, locale, state)
