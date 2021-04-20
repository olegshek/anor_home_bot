from modeltranslation import translator

from apps.bot.models import Button, Message
from apps.file.models import Photo, Video, Document
from core.translation import TranslationOptionsMixin


@translator.register(Photo)
class PhotoOptions(TranslationOptionsMixin):
    fields = ('description', )


@translator.register(Video)
class VideoOptions(TranslationOptionsMixin):
    fields = ('description', )


@translator.register(Document)
class DocumentOptions(TranslationOptionsMixin):
    fields = ('description', )
