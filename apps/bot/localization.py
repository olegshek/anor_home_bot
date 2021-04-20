import gettext
from typing import Tuple, Any, Dict

from aiogram import types
from aiogram.contrib.middlewares.i18n import I18nMiddleware
from django.conf import settings

from apps.lead.tortoise_models import Customer


class Localization(I18nMiddleware):
    async def get_user_locale(self, action: str, args: Tuple[Any]) -> str:
        user: types.User = types.User.get_current()

        *_, data = args
        if not user:
            language = data['locale'] = 'ru'
            return language

        customer = await Customer.filter(id=user.id).first()
        language = data['locale'] = customer.language if customer and customer.language else 'ru'
        return language

    def find_locales(self) -> Dict[str, gettext.GNUTranslations]:
        translation_list = {}
        paths = self.path
        for path in paths:
            self.path = path
            try:
                translation_list.update(super(Localization, self).find_locales())
            except FileNotFoundError:
                continue

        return translation_list


i18n = Localization(settings.I18N_DOMAIN, settings.LOCALE_PATHS)