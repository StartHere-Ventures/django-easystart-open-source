import pytest
from marshmallow import ValidationError

from apps.management import serializers


def test_app_name_schema():
    valid_data = {
        "appName": "Test Name",
    }

    error = {}
    app_name_schema = serializers.SystemAppNameSchema()
    try:
        serializer = app_name_schema.load(valid_data)
    except ValidationError as error_schema:
        error = error_schema.messages

    assert serializer == valid_data
    assert error == {}


def test_invalid_app_name_schema():
    valid_data = {}

    error = {}
    app_name_schema = serializers.SystemAppNameSchema()
    try:
        app_name_schema.load(valid_data)
    except ValidationError as error_schema:
        error = error_schema.messages

    assert error == {"appName": ["Missing data for required field."]}


def test_empty_name_app_name_schema():
    valid_data = {
        "appName": "",
    }

    error = {}
    app_name_schema = serializers.SystemAppNameSchema()
    try:
        app_name_schema.load(valid_data)
    except ValidationError as error_schema:
        error = error_schema.messages

    assert error == {"appName": ["Shorter than minimum length 1."]}


def test_expire_time_schema():
    valid_data = {
        "sessionExpireTime": 60,
    }

    error = {}
    expire_time_schema = serializers.SystemExpireTimeSchema()
    try:
        serializer = expire_time_schema.load(valid_data)
    except ValidationError as error_schema:
        error = error_schema.messages

    assert serializer == valid_data
    assert error == {}


def test_invalid_expire_time_schema():
    valid_data = {}

    error = {}
    expire_time_schema = serializers.SystemExpireTimeSchema()
    try:
        expire_time_schema.load(valid_data)
    except ValidationError as error_schema:
        error = error_schema.messages

    assert error == {"sessionExpireTime": ["Missing data for required field."]}


def test_empty_time_expire_time_schema():
    valid_data = {
        "sessionExpireTime": "",
    }

    error = {}
    expire_time_schema = serializers.SystemExpireTimeSchema()
    try:
        expire_time_schema.load(valid_data)
    except ValidationError as error_schema:
        error = error_schema.messages

    assert error == {"sessionExpireTime": ["Not a valid integer."]}


@pytest.mark.django_db
def test_account_user_group_schema():
    valid_data = {
        "group": "management",
    }

    error = {}
    account_user_group_schema = serializers.AccountUserGroupSchema()
    try:
        serializer = account_user_group_schema.load(valid_data)
    except ValidationError as error_schema:
        error = error_schema.messages

    assert serializer == valid_data
    assert error == {}


@pytest.mark.django_db
def test_invalid_account_user_group_schema():
    valid_data = {}

    error = {}
    account_user_group_schema = serializers.AccountUserGroupSchema()
    try:
        account_user_group_schema.load(valid_data)
    except ValidationError as error_schema:
        error = error_schema.messages

    assert error == {"group": ["Missing data for required field."]}


@pytest.mark.django_db
def test_empty_account_user_group_schema():
    valid_data = {
        "group": "",
    }

    error = {}
    account_user_group_schema = serializers.AccountUserGroupSchema()
    try:
        account_user_group_schema.load(valid_data)
    except ValidationError as error_schema:
        error = error_schema.messages

    assert error == {"group": ["Invalid user group."]}


def test_settings_script_schema():
    valid_data = {
        "header": "<script>header</script>",
        "body": "<script>body</script>",
        "footer": "<script>footer</script>",
    }

    error = {}
    settings_script_schema = serializers.GlobalSettingsScripts()
    try:
        serializer = settings_script_schema.load(valid_data)
    except ValidationError as error_schema:
        error = error_schema.messages

    assert serializer == valid_data
    assert error == {}


def test_invalid_settings_script_schema():
    valid_data = {}

    error = {}
    settings_script_schema = serializers.GlobalSettingsScripts()
    try:
        settings_script_schema.load(valid_data)
    except ValidationError as error_schema:
        error = error_schema.messages

    assert error == {
        "header": ["Missing data for required field."],
        "body": ["Missing data for required field."],
        "footer": ["Missing data for required field."],
    }


@pytest.mark.django_db
def test_create_user_schema():
    valid_data = {
        "firstName": "Jhon",
        "lastName": "Doe",
        "email": "jhondoe@exmaple.com",
        "group": "customer",
    }

    error = {}
    create_user_schema = serializers.CreateUserSchema()
    try:
        serializer = create_user_schema.load(valid_data)
    except ValidationError as error_schema:
        error = error_schema.messages

    assert serializer == valid_data
    assert error == {}


@pytest.mark.django_db
def test_invalid_create_user_schema():
    valid_data = {}

    error = {}
    create_user_schema = serializers.CreateUserSchema()
    try:
        create_user_schema.load(valid_data)
    except ValidationError as error_schema:
        error = error_schema.messages

    assert error == {
        "firstName": ["Missing data for required field."],
        "lastName": ["Missing data for required field."],
        "email": ["Missing data for required field."],
        "group": ["Missing data for required field."],
    }


@pytest.mark.django_db
def test_empty_email_create_user_schema():
    valid_data = {
        "firstName": "Jhon",
        "lastName": "Doe",
        "email": "",
        "group": "customer",
    }

    error = {}
    create_user_schema = serializers.CreateUserSchema()
    try:
        create_user_schema.load(valid_data)
    except ValidationError as error_schema:
        error = error_schema.messages

    assert error == {
        "email": ["Not a valid email address."],
    }


@pytest.mark.django_db
def test_empty_group_create_user_schema():
    valid_data = {
        "firstName": "Jhon",
        "lastName": "Doe",
        "email": "jhondoe@example.com",
        "group": "",
    }

    error = {}
    create_user_schema = serializers.CreateUserSchema()
    try:
        create_user_schema.load(valid_data)
    except ValidationError as error_schema:
        error = error_schema.messages

    assert error == {
        "group": ["Invalid user group."],
    }
