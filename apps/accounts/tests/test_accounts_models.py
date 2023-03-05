import datetime

import pytest
from django.contrib.auth import get_user_model
from django.utils import timezone

from apps.accounts import app_settings, models


@pytest.mark.django_db
def test_email_address_create():
    User = get_user_model()
    user = User.objects.create_user(email="normal@user.com", password="foo")
    email_address = models.EmailAddress.get_or_create(user, "normal@user.com")

    assert email_address.user == user
    assert email_address.email == "normal@user.com"
    assert not email_address.verified
    assert not email_address.primary


@pytest.mark.django_db
def test_email_address_methods():
    User = get_user_model()
    user = User.objects.create_user(email="normal@user.com", password="foo")
    email_address = models.EmailAddress.get_or_create(user, "normal@user.com")
    email_address.set_as_primary()
    confirmation = email_address.send_confirmation()

    assert email_address.get_primary(user) == "normal@user.com"
    assert not email_address.get_not_primary(user)
    assert type(confirmation) == models.EmailConfirmation


@pytest.mark.django_db
def test_email_confirmation():
    User = get_user_model()
    user = User.objects.create_user(email="normal@user.com", password="foo")
    email_address = models.EmailAddress.get_or_create(user, "normal@user.com")
    email_confirmation = models.EmailConfirmation.create(email_address)

    assert email_confirmation.email_address == email_address
    assert len(email_confirmation.key) == 64
    assert email_confirmation.created
    assert not email_confirmation.sent


@pytest.mark.django_db
def test_email_confirmation_methods():
    User = get_user_model()
    user = User.objects.create_user(email="normal@user.com", password="foo")
    email_address = models.EmailAddress.get_or_create(user, "normal@user.com")
    email_confirmation = models.EmailConfirmation.create(email_address)
    email_confirmation.sent = timezone.now()
    email_confirmation.save()

    cooldown_period = datetime.timedelta(
        seconds=app_settings.EMAIL_CONFIRMATION_COOLDOWN
    )
    assert not email_confirmation.key_expired()
    assert not models.EmailConfirmation.can_send_cooldown_period("normal@user.com")
    assert (
        models.EmailConfirmation.time_to_resend_email("normal@user.com")
        < cooldown_period.total_seconds()
    )


@pytest.mark.django_db
def test_email_confirmation_confirm_email():
    User = get_user_model()
    user = User.objects.create_user(email="normal@user.com", password="foo")
    email_address = models.EmailAddress.get_or_create(user, "normal@user.com")
    email_confirmation = models.EmailConfirmation.create(email_address)
    email_confirmation.sent = timezone.now()
    email_confirmation.save()
    email_confirmation.confirm()

    assert email_address.verified
    assert email_address.primary
