from tortoise import models, fields

from apps.lead import app_name


class Location(models.Model):
    latitude = fields.FloatField(null=True)
    longitude = fields.FloatField(null=True)
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
    about_ru = fields.CharField(max_length=4000, null=True)
    about_en = fields.CharField(max_length=4000, null=True)
    about_uz = fields.CharField(max_length=4000, null=True)

    class Meta:
        abstract = True


class ResidentialProject(Project):
    main_photo = fields.ForeignKeyField('file.Photo', on_delete=fields.SET_NULL, null=True,
                                        related_name='residential_projects_main')
    photos = fields.ManyToManyField('file.Photo', related_name='residential_projects',
                                    through='lead_residentialproject_photos',
                                    backward_key='residentialproject_id')
    documents = fields.ManyToManyField('file.Document', related_name='residential_projects',
                                       through='lead_residentialproject_documents',
                                       backward_key='residentialproject_id')
    location = fields.OneToOneField(f'{app_name}.Location', on_delete=fields.SET_NULL, null=True,
                                    related_name='residential_project')
    catalogue_documents = fields.ManyToManyField(f'file.Document',
                                                 related_name='catalogue_residential_projects',
                                                 through='lead_residentialproject_catalogue_documents',
                                                 backward_key='residentialproject_id')

    class Meta:
        table = f'{app_name}_residentialproject'


class CommercialProject(Project):
    main_photo = fields.ForeignKeyField('file.Photo', on_delete=fields.SET_NULL, null=True,
                                        related_name='residential_commercial_main')
    photos = fields.ManyToManyField('file.Photo', related_name='commercial_projects',
                                    through='lead_commercialproject_photos',
                                    backward_key='commercialproject_id')
    documents = fields.ManyToManyField('file.Document', related_name='commercial_projects',
                                       through='lead_commercialproject_documents',
                                       backward_key='commercialproject_id')
    location = fields.OneToOneField(f'{app_name}.Location', on_delete=fields.SET_NULL, null=True,
                                    related_name='commercial_project')
    catalogue_documents = fields.ManyToManyField(f'file.Document',
                                                 related_name='catalogue_commercial_projects',
                                                 through='lead_commercialproject_catalogue_documents',
                                                 backward_key='commercialproject_id')

    class Meta:
        table = f'{app_name}_commercialproject'


class Duplex(models.Model):
    project = fields.ForeignKeyField(f'{app_name}.ResidentialProject', on_delete=fields.CASCADE,
                                     related_name='duplexes')
    room_quantity = fields.IntField()

    class Meta:
        table = f'{app_name}_duplex'


class Apartment(models.Model):
    project = fields.ForeignKeyField(f'{app_name}.ResidentialProject', on_delete=fields.CASCADE,
                                     related_name='apartments')
    duplex = fields.ForeignKeyField(f'{app_name}.Duplex', on_delete=fields.SET_NULL, null=True,
                                    related_name='apartments')
    room_quantity = fields.IntField(null=True)
    square = fields.FloatField()
    description_ru = fields.CharField(max_length=198)
    description_en = fields.CharField(max_length=198)
    description_uz = fields.CharField(max_length=198)

    floor_number = fields.IntField(null=True)

    photo = fields.ForeignKeyField('file.Photo', on_delete=fields.SET_NULL, null=True, related_name='apartments')

    class Meta:
        table = f'{app_name}_apartment'


class Store(models.Model):
    project = fields.ForeignKeyField(f'{app_name}.CommercialProject', on_delete=fields.CASCADE, related_name='stores')
    floor_number = fields.IntField()
    square = fields.FloatField()
    description_ru = fields.CharField(max_length=198)
    description_en = fields.CharField(max_length=198)
    description_uz = fields.CharField(max_length=198)

    photo = fields.ForeignKeyField('file.Photo', on_delete=fields.SET_NULL, null=True, related_name='stores')

    class Meta:
        table = f'{app_name}_store'
