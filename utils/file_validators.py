from django.core.exceptions import ValidationError
from django.core.files.images import get_image_dimensions
from django.utils.translation import gettext_lazy as _


class FileSizeValidator(object):
    def __init__(self, max_size=None):
        if max_size is not None:
            self.max_size = max_size
        else:
            raise TypeError(_("You must provide the max_size flag."))

    def __call__(self, value):
        if value.size > self.max_size:
            raise ValidationError(
                _("The file exceeds the maximum of %(max_size)s MB.")
                % {"max_size": self.max_size / 1024 / 1024}
            )


class ImageDimensionsValidator(object):
    def __init__(self, max_width=None, max_height=None):
        if max_width is not None and max_height is not None:
            self.max_width = max_width
            self.max_height = max_height
        else:
            raise TypeError(_("You must provide the max_width and max_height flag."))

    def __call__(self, value):
        width, height = get_image_dimensions(value)
        content_type = value.content_type

        image_content_types = ["image/png", "image/jpg", "image/jpeg"]

        if content_type in image_content_types:
            if width > self.max_width or height > self.max_height:
                raise ValidationError(
                    _(
                        "The image file exceeds the maximum resolution "
                        "of %(max_width)ix%(max_height)i pixels."
                    )
                    % {"max_width": self.max_width, "max_height": self.max_height}
                )
