from django import forms
from django.contrib.auth.forms import UserChangeForm, UserCreationForm

from utils.file_validators import FileSizeValidator

from . import app_settings, models


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = models.CustomUser
        fields = ("email",)


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = models.CustomUser
        fields = ("email",)


class ProfilePhotoForm(forms.Form):
    photo = forms.FileField(
        validators=[
            FileSizeValidator(max_size=int(app_settings.MAX_SIZE_FILE) * 1024 * 1024),
        ],
    )

    def clean_photo(self):
        valid_content_types = ["image/png", "image/jpg", "image/jpeg"]

        if self.cleaned_data["photo"]:
            photo = self.cleaned_data["photo"]
            content_type = photo.content_type
            if content_type not in valid_content_types:
                raise forms.ValidationError(
                    "Invalid file type, please choose another one."
                )
        else:
            raise forms.ValidationError("This field is required.")

        return self.cleaned_data["photo"]
