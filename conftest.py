import os
from pathlib import Path
from typing import List, Union

import pytest
from django.conf import settings
from django.contrib.auth.models import Group, Permission
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.management import call_command
from django.test import Client

BASE_DIR = Path(__file__).resolve().parent.parent


@pytest.fixture(scope="session")
@pytest.mark.django_db
def django_db_setup(django_db_blocker):
    settings.DATABASES["default"] = {
        "ENGINE": os.environ.get("DB_TEST_ENGINE", "django.db.backends.sqlite3"),
        "HOST": os.environ.get("DB_TEST_HOST", "localhost"),
        "NAME": os.environ.get("DB_TEST_NAME", os.path.join(BASE_DIR, "db.sqlite3")),
        "PORT": os.environ.get("DB_TEST_PORT", "5432"),
        "USER": os.environ.get("DB_TEST_USER", "user"),
        "PASSWORD": os.environ.get("DB_TEST_PASSWORD", "password"),
    }

    with django_db_blocker.unblock():
        call_command("migrate", "--noinput")
        call_command("loaddata", "fixtures/001_groups.json")
        call_command("loaddata", "fixtures/002_create_initial_users.json")
        call_command("runscript", "sync_permissions")


@pytest.fixture
def inertia_client():
    client = Client(HTTP_X_REQUESTED_WITH="XMLHttpRequest", HTTP_X_INERTIA=True)
    return client


@pytest.fixture
def test_password():
    return "Qwer.1234"


@pytest.fixture
def test_image_file():
    content = bytes("some random data", "UTF-8")
    return SimpleUploadedFile("image.jpg", content=content, content_type="image/jpeg")


@pytest.fixture
def create_user(db, django_user_model, test_password):
    def make_user(**kwargs):
        kwargs["password"] = test_password
        if "email" not in kwargs:
            kwargs["email"] = "jhondoe@test.com"
        user = django_user_model.objects.create_user(**kwargs)
        group = Group.objects.get(name="customer")
        group.user_set.add(user)
        return user

    return make_user


@pytest.fixture
def create_manager_user(db, django_user_model, test_password):
    def make_user(**kwargs):
        kwargs["password"] = test_password
        if "email" not in kwargs:
            kwargs["email"] = "jhondoe@test.com"
        user = django_user_model.objects.create_user(**kwargs)
        group = Group.objects.get(name="management")
        group.user_set.add(user)
        return user

    return make_user


@pytest.fixture
def create_custom_user(db, django_user_model, test_password):
    def make_user(**kwargs):
        kwargs["password"] = test_password
        if "email" not in kwargs:
            kwargs["email"] = "jhondoe@test.com"
        user = django_user_model.objects.create_user(**kwargs)
        group, created = Group.objects.get_or_create(name="custom")
        group.user_set.add(user)
        return user

    return make_user


@pytest.fixture
def auto_login_user(db, inertia_client, create_user, test_password):
    def make_auto_login(user=None):
        if user is None:
            user = create_user()
        inertia_client.login(email=user.email, password=test_password)
        return inertia_client, user

    return make_auto_login


@pytest.fixture
def auto_login_manager_user(db, inertia_client, create_manager_user, test_password):
    def make_auto_login(user=None):
        if user is None:
            user = create_manager_user()
        inertia_client.login(email=user.email, password=test_password)
        return inertia_client, user

    return make_auto_login


@pytest.fixture
def auto_login_custom_user(db, inertia_client, create_custom_user, test_password):
    def make_auto_login(user=None):
        if user is None:
            user = create_custom_user()
        inertia_client.login(email=user.email, password=test_password)
        return inertia_client, user

    return make_auto_login


@pytest.fixture
def grant_permissions_custom_group(db):
    def grant_perms(permissions: Union[str, List[str]], app_label: str = "core"):
        custom_group = Group.objects.get(name="custom")
        if isinstance(permissions, str):
            permissions = [permissions]
        for permission_codename in permissions:
            permission = Permission.objects.get(
                codename=permission_codename, content_type__app_label=app_label
            )
            custom_group.permissions.add(permission)

    return grant_perms
