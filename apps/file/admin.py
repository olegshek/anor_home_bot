from django.contrib import admin

from apps.file.models import Photo, Video, Document

admin.site.register(Photo)
admin.site.register(Video)
admin.site.register(Document)
