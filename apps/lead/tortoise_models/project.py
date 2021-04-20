from tortoise import models, fields

from apps.lead import app_name


class Location(models.Model):
    latitude = fields.FloatField()
    longitude = fields.FloatField()
    description_ru = fields.CharField(max_length=4000)
    description_uz = fields.CharField(max_length=4000)
    description_en = fields.CharField(max_length=4000)

    class Meta:
        table = f'{app_name}_location'


class Project(models.Model):
    name = fields.CharField(max_length=48)
    description_ru = fields.CharField(max_length=150)
    description_uz = fields.CharField(max_length=150)
    description_en = fields.CharField(max_length=150)

    class Meta:
        abstract = True


class ResidentialProject(Project):
    main_photo = fields.ForeignKeyField('file.Photo', on_delete=fields.SET_NULL, null=True,
                                        related_name='residential_projects_main')
    photos = fields.ManyToManyField('file.Photo', related_name='residential_projects',
                                    through='lead_residentialproject_photos')
    videos = fields.ManyToManyField('file.Video', related_name='residential_projects',
                                    through='lead_residentialproject_videos')
    documents = fields.ManyToManyField('file.Document', related_name='residential_projects',
                                       through='lead_residentialproject_documents')
    location = fields.OneToOneField(f'{app_name}.Location', on_delete=fields.SET_NULL, null=True,
                                    related_name='residential_project')
    catalog_documents = fields.ManyToManyField(f'file.Document',
                                               related_name='document_residential_projects',
                                               through='lead_residentialproject_catalog_documents')

    class Meta:
        table = f'{app_name}_residentialproject'


class CommercialProject(Project):
    main_photo = fields.ForeignKeyField('file.Photo', on_delete=fields.SET_NULL, null=True,
                                        related_name='residential_commercial_main')
    photos = fields.ManyToManyField('file.Photo', related_name='commercial_projects',
                                    through='lead_commercialproject_photos')
    videos = fields.ManyToManyField('file.Video', related_name='commercial_projects',
                                    through='lead_commercialproject_videos')
    documents = fields.ManyToManyField('file.Document', related_name='commercial_projects',
                                       through='lead_commercialproject_documents')
    location = fields.OneToOneField(f'{app_name}.Location', on_delete=fields.SET_NULL, null=True,
                                    related_name='commercial_project')
    catalog_documents = fields.ManyToManyField(f'file.Document',
                                               related_name='document_commercial_projects',
                                               through='lead_commercialproject_catalog_documents')

    class Meta:
        table = f'{app_name}_commercialproject'


class Apartment(models.Model):
    project = fields.ForeignKeyField(f'{app_name}.ResidentialProject', on_delete=fields.CASCADE,
                                     related_name='apartments')
    room_quantity = fields.IntField()
    square = fields.FloatField()
    description_ru = fields.CharField(max_length=198)
    description_en = fields.CharField(max_length=198)
    description_uz = fields.CharField(max_length=198)

    photos = fields.ManyToManyField('file.Photo', related_name='apartments', through='lead_apartment_photos',
                                    backward_key='apartment_id')

    class Meta:
        table = f'{app_name}_apartment'


class Store(models.Model):
    project = fields.ForeignKeyField(f'{app_name}.CommercialProject', on_delete=fields.CASCADE, related_name='stores')
    floor_number = fields.IntField()
    square = fields.FloatField()
    description_ru = fields.CharField(max_length=198)
    description_en = fields.CharField(max_length=198)
    description_uz = fields.CharField(max_length=198)

    photos = fields.ManyToManyField('file.Photo', related_name='stores', through='lead_store_photos',
                                    backward_key='store_id')

    class Meta:
        table = f'{app_name}_store'
