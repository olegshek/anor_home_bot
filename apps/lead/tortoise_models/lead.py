from django.utils import timezone
from tortoise import models, fields

from apps.lead import app_name
from core.utils import generate_number


class Lead(models.Model):
    number = fields.IntField(default=generate_number)
    customer = fields.ForeignKeyField(f'{app_name}.Customer', on_delete=fields.CASCADE, related_name='leads')

    created_at = fields.DatetimeField(default=timezone.now, blank=True, editable=False)

    class Meta:
        table = f'{app_name}_lead'


class ApartmentTransaction(models.Model):
    customer = fields.ForeignKeyField(f'{app_name}.Customer', on_delete=fields.CASCADE,
                                      related_name='apartment_transactions')
    lead = fields.ForeignKeyField(f'{app_name}.Lead', on_delete=fields.CASCADE, null=True,
                                  related_name='apartment_transactions')
    apartment = fields.ForeignKeyField(f'{app_name}.Apartment', on_delete=fields.CASCADE,
                                       related_name='apartment_transactions')

    created_at = fields.DatetimeField(default=timezone.now, blank=True, editable=False)

    class Meta:
        table = f'{app_name}_apartmenttransaction'


class StoreTransaction(models.Model):
    customer = fields.ForeignKeyField(f'{app_name}.Customer', on_delete=fields.CASCADE,
                                      related_name='store_transactions')
    lead = fields.ForeignKeyField(f'{app_name}.Lead', on_delete=fields.CASCADE, null=True,
                                  related_name='store_transactions')
    apartment = fields.ForeignKeyField(f'{app_name}.Apartment', on_delete=fields.CASCADE,
                                       related_name='store_transactions')

    created_at = fields.DatetimeField(default=timezone.now, blank=True, editable=False)

    class Meta:
        table = f'{app_name}_storetransaction'
