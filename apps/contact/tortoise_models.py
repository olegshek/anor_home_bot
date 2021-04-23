from tortoise import models, fields


class ContactLocation(models.Model):
    location = fields.OneToOneField('lead.Location', on_delete=fields.CASCADE, related_name='contact_location')


class ContactText(models.Model):
    text_ru = fields.CharField(max_length=4000)
    text_en = fields.CharField(max_length=4000)
    text_uz = fields.CharField(max_length=4000)


class ContactPhoto(models.Model):
    photo = fields.OneToOneField('file.Photo', on_delete=fields.CASCADE, related_name='contact_photo')
