from django.apps import apps
from django.contrib.auth.models import Group
from django.template import TemplateDoesNotExist

from utils.email import EMail


def get_groups():
    availableGroups = {g.name: g.name for g in Group.objects.all()}

    return availableGroups


def is_audit_installed():
    return apps.is_installed("apps.audit")


def send_mail(subject, template_prefix, email, context):
    msg = EMail(to=email, subject=subject)
    try:
        msg.html(f"{template_prefix}_message.html", context)
    except TemplateDoesNotExist:
        pass

    msg.text(f"{template_prefix}_message.txt", context)
    msg.send()
