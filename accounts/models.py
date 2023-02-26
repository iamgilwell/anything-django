import uuid
from django.db import models
from django.conf import settings
from core.mixins.GenericMixin import AddressMixin

from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.core.mail import send_mail


def company_logo(instance, filename):
    return 'media/company_logo_/{0}/{1}'.format(instance.slug, filename)

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, is_active=False):
        if not email:
            raise ValueError("Users must have an email address")
        if not password:
            raise ValueError("Users must have a password")
        user_obj = self.model(email=self.normalize_email(email),)
        user_obj.set_password(password)
        user_obj.active = is_active
        user_obj.confirmed_email = False
        user_obj.save()
        return user_obj

    def create_superuser(self, email, password=None):
        user = self.create_user(email, password=password)
        user.admin = True
        user.staff = True
        user.active = True
        user.save()

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=255, unique=True)
    slug = models.SlugField(max_length=255,null=True, blank=True)
    active = models.BooleanField(
        default=False
    )  # allows login - set after email confirmation
    staff = models.BooleanField(default=False)  # staff user non superuser
    admin = models.BooleanField(default=False)  # superuser
    confirmed_email = models.BooleanField(default=False)


    objects = UserManager()
    USERNAME_FIELD = "email"
    EMAIL_FIELD = "email"

    def save(self, **kwargs):
        if not self.slug:
            self.slug = uuid.uuid4()
        super().save(**kwargs)

    def __str__(self):
        return self.email

    def get_full_name(self):
        return "{} {}".format(self.user_profile.first_name,self.user_profile.last_name)

    def get_short_name(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_admin(self):
        return self.admin

    @property
    def is_active(self):
        return self.active

    @property
    def is_staff(self):
        return self.staff

class Profile(AddressMixin,models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,related_name='user_profile', primary_key=True, on_delete=models.CASCADE
    )
    first_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)

    def email_user(self, *args, **kwargs):
        send_mail(
            "Subject here",
            "Here is the message.",
            ["gilwell@anythingdjango.com"],
            [self.user.email],
            fail_silently=False,
        )

    def __str__(self):
        return "{} {}".format(self.user.get_username(), self.first_name, self.last_name)

