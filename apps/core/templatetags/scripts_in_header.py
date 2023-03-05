"""
    Third Part Platform template tags
    =======================

    This module defines the template tags that can be used to include functions and catalog sets
    of Third Part Platforms in Django templates.

"""
from django import template
from django.template import Context, Engine

from apps.core.models import GlobalSettings

register = template.Library()


@register.simple_tag
def header_scripts():
    """Includes the serialized version of the exposed third part platforms in the template."""
    scripts = ""

    global_settings = GlobalSettings.objects.filter()
    if global_settings:
        scripts = global_settings.first().header_scripts

    context = {
        "scripts": scripts,
    }
    html = r"""
        {% autoescape off %}
            {% if scripts %}
                {{ scripts }}
            {% endif %}
        {% endautoescape %}
    """
    template = Engine().from_string(html)
    return template.render(Context(context))
