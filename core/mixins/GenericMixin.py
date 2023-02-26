
from django.db import models
from django_countries.fields import CountryField

class AddressMixin(models.Model):
    phone = models.CharField(max_length=100, null=True, blank=True, unique=True)
    email = models.EmailField(max_length=150,null=True, blank=True, unique=True)
    bio = models.TextField(max_length=20000, null=True, blank=True,)
    country = CountryField(blank=True,null=True)
    # city = models.CharField(max_length=100, null=True, blank=True)
    state = models.CharField(max_length=100, null=True, blank=True,)
    zip_code = models.CharField(max_length=100, null=True, blank=True,)

    def country_name(self):
        return str(self.country.name)

    class Meta:
        abstract = True

class SocialNetWorkMixin(models.Model):
    facebook = models.CharField(max_length=100, null=True, blank=True, unique=True)
    twitter = models.CharField(max_length=150,null=True, blank=True, unique=True)
    linkedin = models.CharField(max_length=150, null=True, blank=True,)
    youtube = models.CharField(max_length=150, null=True, blank=True,)

    class Meta:
        abstract = True
