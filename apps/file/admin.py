from django.contrib import admin
from modeltranslation.admin import TranslationAdmin

from apps.file.forms import PhotoForm, DocumentForm
from apps.file.models import Photo, Document


class PhotoAdmin(TranslationAdmin):
    form = PhotoForm


class DocumentAdmin(TranslationAdmin):
    form = DocumentForm


admin.site.register(Photo, PhotoAdmin)
admin.site.register(Document, DocumentAdmin)
