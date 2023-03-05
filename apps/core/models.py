import base64
import os

from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import IntegrityError, models
from django_countries.fields import CountryField
from model_utils.models import TimeStampedModel

from .managers import CustomUserManager


class CustomUser(AbstractUser):
    username = None
    email = models.EmailField("email address", unique=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    class Meta:
        verbose_name = "user"
        verbose_name_plural = "users"

    def __str__(self):
        return self.email

    @classmethod
    def create_user(
        cls, email: str, password: str, first_name: str = "", last_name: str = ""
    ):
        user_exist = CustomUser.objects.filter(email=email)
        if user_exist:
            raise ValueError("User already exist")

        user = cls()
        user.email = email
        user.first_name = first_name
        user.last_name = last_name
        user.set_password(password)
        try:
            user.save()
        except IntegrityError:
            raise ValueError("User already exist")

        return user


def user_profile_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/application_<id>/<filename>
    return "profile/photo_{0}/{1}".format(str(instance.user.id), filename)


class UserProfile(TimeStampedModel):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    photo = models.FileField(
        upload_to=user_profile_directory_path, null=True, blank=True
    )
    job_title = models.CharField(max_length=255, null=True, blank=True)
    language = models.CharField(max_length=5, default="en-us")
    country = CountryField(null=True, blank=True)
    date_format = models.CharField(max_length=15, default="dd-mm-yyyy", blank=True)

    def __str__(self):
        return f"User Profile {self.user}"

    def get_photo(self):
        if self.photo:
            image_path = os.path.join(settings.MEDIA_ROOT, self.photo.name)

            with open(image_path, "rb") as img_f:
                encoded_string = base64.b64encode(img_f.read()).decode("ascii")

            return "data:image/png;base64,%s" % (encoded_string)

        else:
            return "/static/img/photo_default.png"


def global_settings_logo_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/application_<id>/<filename>
    return "settings/logo_{0}/{1}".format(str(instance.id), filename)


class GlobalSettings(TimeStampedModel):
    name_app = models.CharField(max_length=255, default="", blank=True)
    logo_app = models.FileField(
        upload_to=global_settings_logo_directory_path, null=True, blank=True
    )
    session_expire_time = models.IntegerField(default=60)
    active_registration = models.BooleanField(default=True)
    header_scripts = models.TextField(blank=True, null=True)
    footer_scripts = models.TextField(blank=True, null=True)
    body_scripts = models.TextField(blank=True, null=True)

    def get_logo(self):
        if self.logo_app:
            image_path = os.path.join(settings.MEDIA_ROOT, self.logo_app.name)

            with open(image_path, "rb") as img_f:
                encoded_string = base64.b64encode(img_f.read()).decode("ascii")

            return "data:image/png;base64,%s" % (encoded_string)

        else:
            return "/static/img/logo.png"
