from celery import shared_task
from celery.utils.log import get_task_logger
from django.contrib.sites.shortcuts import get_current_site
from django.db import transaction
from django.utils import timezone, translation

from apps.core import models as core_models
from apps.core.utils import send_mail

from . import app_settings, models, utils

logger = get_task_logger(__name__)


def email_confirmation(
    request, user, signup: bool = False, email: str = None, change: bool = False
):
    email_address = models.EmailAddress.get_or_create(user, email)

    if app_settings.EMAIL_VERIFICATION == app_settings.EmailVerificationMethod.NONE:
        return None

    models.EmailConfirmation.delete_old_emails(email_address)
    confirmation = models.EmailConfirmation.create(email_address)

    current_site = get_current_site(request)
    activate_url = utils.get_email_confirmation_url(request, confirmation)
    lang = translation.get_language()
    transaction.on_commit(
        lambda: send_email_confirmation.delay(
            str(confirmation.id),
            email_address.user.email,
            current_site.name,
            activate_url,
            signup,
            change,
            lang,
        )
    )
    confirmation.sent = timezone.now()
    confirmation.save()


def email_password_reset(request, user):
    current_site = get_current_site(request)
    url = utils.generate_url_password_reset(request, user)
    lang = translation.get_language()
    send_email_password_reset.delay(str(user.id), current_site.name, url, lang)


@shared_task(name="default:send_email_confirmation")
def send_email_confirmation(
    confirm_id,
    user_email,
    site_name,
    activate_url,
    signup: bool = False,
    change: bool = False,
    lang: str = "en-us",
):
    emailconfirmation = models.EmailConfirmation.objects.get(id=confirm_id)

    # Send email through console or SMTP
    ctx = {
        "user": user_email,
        "email": emailconfirmation.email_address.email,
        "activate_url": activate_url,
        "site_name": site_name,
        "key": emailconfirmation.key,
        "lang": lang,
    }
    if signup:
        email_template = "email/email_confirmation_signup"
    elif change:
        email_template = "email/change_email_confirmation"
    else:
        email_template = "email/email_confirmation"
    subject = "Please Confirm Your E-mail Address"
    send_mail(subject, email_template, emailconfirmation.email_address.email, ctx)


@shared_task(name="default:send_email_password_reset")
def send_email_password_reset(user_id, site_name, url, lang: str = "en-us"):
    user = core_models.CustomUser.objects.get(id=user_id)

    # Send email through console or SMTP
    ctx = {
        "site_name": site_name,
        "user": user,
        "password_reset_url": url,
        "lang": lang,
    }
    email_template = "email/password_reset_key"
    subject = "Password Reset E-mail"
    send_mail(subject, email_template, user.email, ctx)
