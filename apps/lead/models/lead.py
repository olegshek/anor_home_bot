from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from apps.lead.models import Customer, Apartment, Store
from apps.lead.models.project import Duplex
from core.utils import generate_number


class Lead(models.Model):
    number = models.IntegerField(default=generate_number, verbose_name=_('Number'))
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='leads', verbose_name=_('Customer'))

    created_at = models.DateTimeField(default=timezone.now, blank=True, editable=False)

    class Meta:
        ordering = ('-created_at',)
        verbose_name = _('Lead')
        verbose_name_plural = _('Leads')

    def __str__(self):
        return str(self.number)


class ApartmentTransaction(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='apartment_transactions',
                                 verbose_name=_('Customer'))
    lead = models.ForeignKey(Lead, on_delete=models.CASCADE, null=True, related_name='apartment_transactions',
                             verbose_name=_('Lead'))
    apartment = models.ForeignKey(Apartment, on_delete=models.CASCADE, related_name='transactions',
                                  verbose_name=_('apartment'))

    created_at = models.DateTimeField(default=timezone.now, blank=True, editable=False)

    class Meta:
        verbose_name = _('Apartment transaction')
        verbose_name_plural = _('Apartment transactions')

    def __str__(self):
        return self.apartment.__str__()


class StoreTransaction(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='store_transactions',
                                 verbose_name=_('Customer'))
    lead = models.ForeignKey(Lead, on_delete=models.CASCADE, null=True, related_name='store_transactions',
                             verbose_name=_('Lead'))
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name='transactions', verbose_name=_('Store'))
    created_at = models.DateTimeField(default=timezone.now, blank=True, editable=False)

    class Meta:
        verbose_name = _('Store transaction')
        verbose_name_plural = _('Store transactions')

    def __str__(self):
        return self.store.__str__()


class DuplexTransaction(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='duplex_transactions',
                                 verbose_name=_('Customer'))
    lead = models.ForeignKey(Lead, on_delete=models.CASCADE, null=True, related_name='duplex_transactions',
                             verbose_name=_('Lead'))
    duplex = models.ForeignKey(Duplex, on_delete=models.CASCADE, related_name='transactions', verbose_name=_('Duplex'))

    created_at = models.DateTimeField(default=timezone.now, blank=True, editable=False)

    class Meta:
        verbose_name = _('Duplex transaction')
        verbose_name_plural = _('Duplex transactions')

    def __str__(self):
        return self.duplex.__str__()
