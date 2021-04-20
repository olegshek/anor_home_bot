from enum import Enum

from django.utils import timezone
from tortoise import models, fields

from apps.lead import app_name
from core.utils import generate_number


class Customer(models.Model):
    class Languages(str, Enum):
        RU = 'ru'
        UZ = 'uz'
        EN = 'en'

    id = fields.IntField(pk=True)
    username = fields.CharField(max_length=20, blank=True, null=True)
    full_name = fields.CharField(max_length=200, null=True, blank=True)
    phone_number = fields.CharField(max_length=20, null=True)
    language = fields.CharField(max_length=2, choices=Languages, null=True)

    class Meta:
        table = f'{app_name}_customer'


class Feedback(models.Model):
    number = fields.IntField(default=generate_number)
    customer = fields.ForeignKeyField(f'{app_name}.Customer', on_delete=fields.CASCADE, related_name='feedback')

    created_at = fields.DatetimeField(default=timezone.now, blank=True, editable=False)
    updated_at = fields.DatetimeField(auto_now=True)

    class Meta:
        table = f'{app_name}_feedback'

