import pytest
from django.contrib.auth import get_user_model

from apps.core import models


@pytest.mark.django_db
def test_create_user():
    User = get_user_model()
    user = User.objects.create_user(email="normal@user.com", password="foo")

    assert user.email == "normal@user.com"
    assert user.is_active
    assert not user.is_staff
    assert not user.is_superuser


@pytest.mark.django_db
def test_create_superuser():
    User = get_user_model()
    admin_user = User.objects.create_superuser(email="super@user.com", password="foo")

    assert admin_user.email == "super@user.com"
    assert admin_user.is_active
    assert admin_user.is_staff
    assert admin_user.is_superuser


@pytest.mark.django_db
def test_user_profile_model():
    User = get_user_model()
    user = User.objects.create_user(email="normal@user.com", password="foo")
    user_profile = models.UserProfile(
        user=user, job_title="developer", language="es", country="ES"
    )
    user_profile.save()

    assert user_profile.job_title == "developer"
    assert user_profile.language == "es"
    assert user_profile.country == "ES"
    assert user_profile.date_format == "dd-mm-yyyy"
    assert not user_profile.photo
    assert user_profile.get_photo() == "/static/img/photo_default.png"
    assert user_profile.created


@pytest.mark.django_db
def test_global_settings_model():
    g_settings = models.GlobalSettings(
        name_app="app",
        header_scripts="header",
        footer_scripts="footer",
        body_scripts="body",
    )
    g_settings.save()

    assert g_settings.name_app == "app"
    assert not g_settings.logo_app
    assert g_settings.session_expire_time == 60
    assert g_settings.header_scripts == "header"
    assert g_settings.footer_scripts == "footer"
    assert g_settings.body_scripts == "body"
    assert g_settings.get_logo() == "/static/img/logo.png"
    assert g_settings.created
