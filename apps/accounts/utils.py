from urllib.parse import urlsplit

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.models import Site
from django.core.exceptions import ValidationError
from django.db import models as db_models
from django.urls import reverse
from django.utils.http import base36_to_int, int_to_base36

from . import app_settings


def get_params_password_validator():
    params = []
    for validator in settings.AUTH_PASSWORD_VALIDATORS:
        if "IDENTIFIER" in validator:
            params.append(validator["IDENTIFIER"])

    return params


def build_absolute_uri(request, location, protocol=None):
    """request.build_absolute_uri() helper

    Like request.build_absolute_uri, but gracefully handling
    the case where request is None.
    """

    if request is None:
        site = Site.objects.get_current()
        bits = urlsplit(location)
        if not (bits.scheme and bits.netloc):
            uri = "{proto}://{domain}{url}".format(
                proto=app_settings.DEFAULT_HTTP_PROTOCOL,
                domain=site.domain,
                url=location,
            )
        else:
            uri = location
    else:
        uri = request.build_absolute_uri(location)
    # NOTE: We only force a protocol if we are instructed to do so
    # (via the `protocol` parameter, or, if the default is set to
    # HTTPS. The latter keeps compatibility with the debatable use
    # case of running your site under both HTTP and HTTPS, where one
    # would want to make sure HTTPS links end up in password reset
    # mails even while they were initiated on an HTTP password reset
    # form.
    if not protocol and app_settings.DEFAULT_HTTP_PROTOCOL == "https":
        protocol = app_settings.DEFAULT_HTTP_PROTOCOL
    # (end NOTE)
    if protocol:
        uri = protocol + ":" + uri.partition(":")[2]
    return uri


def get_email_confirmation_url(request, emailconfirmation):
    """Constructs the email confirmation (activation) url.

    Note that if you have architected your system such that email
    confirmations are sent outside of the request context `request`
    can be `None` here.
    """
    url = reverse("accounts:confirm_email", args=[emailconfirmation.key])
    ret = build_absolute_uri(request, url)
    return ret


def generate_url_password_reset(request, user):
    token_generator = default_token_generator
    temp_key = token_generator.make_token(user)
    path = reverse(
        "accounts:reset_password_from_key",
        kwargs=dict(uidb36=user_pk_to_url_str(user), key=temp_key),
    )
    url = build_absolute_uri(request, path)

    return url


def user_pk_to_url_str(user):
    """
    This should return a string.
    """
    User = get_user_model()
    if issubclass(type(User._meta.pk), db_models.UUIDField):
        if isinstance(user.pk, str):
            return user.pk
        return user.pk.hex

    ret = user.pk
    if isinstance(ret, int):
        ret = int_to_base36(user.pk)
    return str(ret)


def url_str_to_user_pk(s):
    User = get_user_model()
    # TODO: Ugh, isn't there a cleaner way to determine whether or not
    # the PK is a str-like field?
    if getattr(User._meta.pk, "remote_field", None):
        pk_field = User._meta.pk.remote_field.to._meta.pk
    else:
        pk_field = User._meta.pk
    if issubclass(type(pk_field), db_models.UUIDField):
        return pk_field.to_python(s)
    try:
        pk_field.to_python("a")
        pk = s
    except ValidationError:
        pk = base36_to_int(s)
    return pk


def get_user_from_uidb36(uidb36):
    User = get_user_model()
    try:
        pk = url_str_to_user_pk(uidb36)
        return User.objects.get(pk=pk)
    except (ValueError, User.DoesNotExist):
        raise ValueError("The password reset token was invalid.")


def custom_password():
    import secrets
    import string

    password_characters = string.ascii_letters + string.digits + ".;*!+"
    return "".join(secrets.choice(password_characters) for i in range(10))
