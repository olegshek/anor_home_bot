from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from apps.lead.models import Customer, Apartment, Store
from core.utils import generate_number


class Lead(models.Model):
    number = models.IntegerField(default=generate_number, verbose_name=_('Number'))
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='leads', verbose_name=_('Customer'))

    created_at = models.DateTimeField(default=timezone.now, blank=True, editable=False)


class ApartmentTransaction(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='apartment_transactions',
                                 verbose_name=_('Customer'))
    lead = models.ForeignKey(Lead, on_delete=models.CASCADE, null=True, related_name='apartment_transactions',
                             verbose_name=_('Lead'))
    apartment = models.ForeignKey(Apartment, on_delete=models.CASCADE, related_name='transactions',
                                  verbose_name=_('apartment'))

    created_at = models.DateTimeField(default=timezone.now, blank=True, editable=False)


class StoreTransaction(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='store_transactions',
                                 verbose_name=_('Customer'))
    lead = models.ForeignKey(Lead, on_delete=models.CASCADE, null=True, related_name='store_transactions',
                             verbose_name=_('Lead'))
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name='transactions', verbose_name=_('Store'))
    created_at = models.DateTimeField(default=timezone.now, blank=True, editable=False)
