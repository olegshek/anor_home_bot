from modeltranslation import translator

from apps.bot.models import Button, Message
from apps.contact.models import ContactText
from core.translation import TranslationOptionsMixin


@translator.register(ContactText)
class ContactTextOptions(TranslationOptionsMixin):
    fields = ('text', )
