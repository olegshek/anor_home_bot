from tortoise import models, fields

from apps.file import app_name


class File(models.Model):
    description_en = fields.CharField(max_length=198)
    description_ru = fields.CharField(max_length=198)
    description_uz = fields.CharField(max_length=198)

    class Meta:
        abstract = True


class Photo(File):
    photo = fields.TextField()

    class Meta:
        table = f'{app_name}_photo'

    def get_path(self):
        return f"media/{self.photo}"


class Document(File):
    document = fields.TextField()

    class Meta:
        table = f'{app_name}_document'

    def get_path(self):
        return f"media/{self.document}"


class Video(File):
    video = fields.TextField()

    class Meta:
        table = f'{app_name}_video'

    def get_path(self):
        return f"media/{self.video}"
