from modeltranslation import translator

from apps.file.models import Photo, Document
from core.translation import TranslationOptionsMixin


@translator.register(Photo)
class PhotoOptions(TranslationOptionsMixin):
    fields = ('description', )


@translator.register(Document)
class DocumentOptions(TranslationOptionsMixin):
    fields = ('description', )
