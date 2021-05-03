from django.contrib import admin

from apps.contact.models import ContactLocation, ContactPhoto, ContactText
from core.admin import TextAdmin

admin.site.register(ContactLocation)
admin.site.register(ContactText, TextAdmin)
admin.site.register(ContactPhoto)
