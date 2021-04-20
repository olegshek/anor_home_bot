from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from apps.lead.models import Customer, Apartment, Store
from core.utils import generate_number


class Lead(models.Model):
    number = models.IntegerField(default=generate_number, verbose_name=_('Number'))
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='leads', verbose_name=_('Customer'))
    apartments = models.ManyToManyField(Apartment, related_name='leads', verbose_name=_('Apartments'))
    stores = models.ManyToManyField(Store, related_name='leads', verbose_name=_('Stores'))

    created_at = models.DateTimeField(default=timezone.now, blank=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True)


class Transaction(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='leads', verbose_name=_('Customer'))
    created_at = models.DateTimeField(default=timezone.now, blank=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class ApartmentTransaction(Transaction):
    apartment = models.ForeignKey(Apartment, on_delete=models.CASCADE, related_name='transactions')


class StoreTransaction(Transaction):
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name='transactions')
