from django.db import models
from django_countries.fields import CountryField
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils import timezone
class TimeStampMixin(models.Model):
    created_at = models.DateTimeField(default=timezone.now, editable=False)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
