from django import forms

from utils.file_validators import FileSizeValidator


class SystemAppLogoForm(forms.Form):
    logo = forms.FileField(
        validators=[
            FileSizeValidator(max_size=int(6) * 1024 * 1024),
        ],
    )

    def clean_logo(self):
        valid_content_types = ["image/png", "image/jpg", "image/jpeg"]

        if self.cleaned_data["logo"]:
            logo = self.cleaned_data["logo"]
            content_type = logo.content_type
            if content_type not in valid_content_types:
                raise forms.ValidationError(
                    "Invalid file type, please choose another one."
                )
        else:
            raise forms.ValidationError("This field is required.")

        return self.cleaned_data["logo"]
