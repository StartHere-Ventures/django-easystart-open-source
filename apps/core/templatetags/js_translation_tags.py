"""
    JS Translation template tags
    =======================

    This module defines the template tags that can be used to include functions and catalog sets of Translation in
    Django templates.

"""
import json
import os

from django import template
from django.conf import settings

register = template.Library()


@register.inclusion_tag("translation.html", takes_context=False)
def js_translation():
    """Includes the serialized version of the exposed translation in the template."""
    path = os.path.join(settings.BASE_DIR, "translation-stats.json")
    stats = json.loads(open(path).read())
    file_name = stats["file"]
    publicPath = stats["publicPath"]
    return {
        "path": f"/{publicPath}/{file_name}",
    }
