from apps.bot import dispatcher as dp, bot, keyboards, messages
from apps.bot.utils import try_delete_message
from apps.company import callback_filters
from apps.company.states import CompanyForm
from apps.company.tortoise_models import CompanyText, CompanyPhoto, CompanyDocument, Service, Vacancy
from apps.lead.callback_filters import choose_button


@dp.callback_query_handler(callback_filters.anorhome_menu, state=CompanyForm.menu.state)
async def anorhome_menu(query, locale, state):
    user_id = query.from_user.id
    message_id = query.message.message_id
    code = query.data

    if code == 'about_company':
        await try_delete_message(user_id, message_id)
        company_text = await CompanyText.first()
        company_photos = await CompanyPhoto.all()
        company_documents = await CompanyDocument.all()

        await bot.send_message(user_id, getattr(company_text, f'text_{locale}'),
                               reply_markup=keyboards.back_keyboard(locale))

        for company_photo in company_photos:
            photo = await company_photo.photo
            with open(photo.get_path(), 'rb') as photo_data:
                await bot.send_photo(
                    user_id,
                    photo_data,
                    caption=getattr(photo, f'description_{locale}'),
                    parse_mode='HTML'
                )

        for company_document in company_documents:
            photo = await company_document.document
            with open(photo.get_path(), 'rb') as photo_data:
                await bot.send_photo(
                    user_id,
                    photo_data,
                    caption=getattr(photo, f'description_{locale}'),
                    parse_mode='HTML'
                )

        await CompanyForm.about.set()

    if code == 'corporate_customer':
        services = await Service.all()
        services_len = len(services)

        for service in services:
            is_last = True if services.index(service) == services_len - 1 else False
            photo = await service.photo
            keyboard = keyboards.services_or_vacancies(service, locale, is_last)

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
            keyboard = keyboards.services_or_vacancies(vacancy, locale, is_last)

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
        name = getattr(service, f'name_{locale}')
        description = getattr(service, f'description_{locale}')
        photo = await service.photo
        keyboard = await keyboards.apply(service_id, locale)
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


