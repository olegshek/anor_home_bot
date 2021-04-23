from tortoise import models, fields

from apps.company import app_name


class CompanyText(models.Model):
    text_ru = fields.CharField(max_length=4000)
    text_uz = fields.CharField(max_length=4000)
    text_en = fields.CharField(max_length=4000)

    class Meta:
        table = f'{app_name}_companytext'


class CompanyPhoto(models.Model):
    photo = fields.OneToOneField('file.Photo', on_delete=fields.CASCADE, related_name='company_photo')

    class Meta:
        table = f'{app_name}_companyphoto'


class CompanyDocument(models.Model):
    document = fields.OneToOneField('file.Document', on_delete=fields.CASCADE, related_name='company_document')

    class Meta:
        table = f'{app_name}_companydocument'


class Service(models.Model):
    name_ru = fields.CharField(max_length=100)
    name_uz = fields.CharField(max_length=100)
    name_en = fields.CharField(max_length=100)
    description_ru = fields.CharField(max_length=200)
    description_uz = fields.CharField(max_length=200)
    description_en = fields.CharField(max_length=200)
    photo = fields.OneToOneField('file.Photo', on_delete=fields.RESTRICT, related_name='service')

    class Meta:
        table = f'{app_name}_service'


class Vacancy(models.Model):
    name_ru = fields.CharField(max_length=100)
    name_uz = fields.CharField(max_length=100)
    name_en = fields.CharField(max_length=100)
    description_ru = fields.CharField(max_length=200)
    description_uz = fields.CharField(max_length=200)
    description_en = fields.CharField(max_length=200)
    photo = fields.OneToOneField('file.Photo', on_delete=fields.RESTRICT, related_name='vacancy')

    class Meta:
        table = f'{app_name}_vacancy'
