from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from core.utils import generate_number


class Customer(models.Model):
    id = models.IntegerField(primary_key=True, editable=False, unique=True)
    username = models.CharField(max_length=20, blank=True, null=True, verbose_name=_('Username'))
    full_name = models.CharField(max_length=200, null=True, blank=True, verbose_name=_('Full name'))
    phone_number = models.CharField(max_length=20, null=True, verbose_name=_('Phone number'))
    language = models.CharField(max_length=2, choices=settings.LANGUAGES, null=True, verbose_name=_('Language'))

    class Meta:
        verbose_name = _('Customer')
        verbose_name_plural = _('Customers')

    def __str__(self):
        return self.full_name if self.full_name else self.phone_number if self.phone_number else self.id


class Feedback(models.Model):
    number = models.IntegerField(default=generate_number)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='feedback',
                                 verbose_name=_('Customer'))

    created_at = models.DateTimeField(default=timezone.now, blank=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True)
