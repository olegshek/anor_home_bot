from apps.bot import dispatcher as dp, bot, keyboards
from apps.lead import callback_filters
from apps.lead.states import LeadForm
from apps.lead.telegram_views.project import send_project_object


@dp.callback_query_handler(callback_filters.add_to_cart, state=LeadForm.project_object_choice)
async def add_to_cart(query, locale, state):
    user_id = query.from_user.id
    object_id = int(query.data.split(';')[1])

    async with state.proxy() as data:
        project_type = data['project_type']
        object_type = 'apartments' if project_type == 'residential' else 'stores'
        saved_objects = data.get(object_type, None)

        if not saved_objects:
            data[object_type] = [object_id]

        else:
            saved_objects.append(object_id)

    await send_project_object(user_id, query.message.message_id, locale, state, object_id)


@dp.callback_query_handler(callback_filters.cart, '*')
async def cart(query, locale, state):
    pass
