import pytest
from django.contrib.auth import get_user_model
from marshmallow import ValidationError

from apps.accounts import serializers, utils


def test_register_schema():
    valid_data = {
        "firstName": "Jhon",
        "lastName": "Doe",
        "email": "jhondoe@test.com",
        "password": "Qwer.1234",
    }

    error = {}
    register_schema = serializers.RegisterSchema()
    try:
        serializer = register_schema.load(valid_data)
    except ValidationError as error_schema:
        error = error_schema.messages

    assert serializer == valid_data
    assert error == {}


def test_empty_register_schema():
    valid_data = {}

    error = {}
    register_schema = serializers.RegisterSchema()
    try:
        register_schema.load(valid_data)
    except ValidationError as error_schema:
        error = error = error_schema.messages

    assert error == {
        "firstName": ["Missing data for required field."],
        "lastName": ["Missing data for required field."],
        "email": ["Missing data for required field."],
        "password": ["Missing data for required field."],
    }


def test_invalid_email_register_schema():
    valid_data = {
        "firstName": "Jhon",
        "lastName": "Doe",
        "email": "",
        "password": "Qwer.1234",
    }

    error = {}
    register_schema = serializers.RegisterSchema()
    try:
        register_schema.load(valid_data)
    except ValidationError as error_schema:
        error = error_schema.messages

    assert error == {"email": ["Not a valid email address."]}


def test_invalid_password_register_schema():
    valid_data = {
        "firstName": "Jhon",
        "lastName": "Doe",
        "email": "jhondoe@test.com",
        "password": "QWER.1234",
    }

    error = {}
    register_schema = serializers.RegisterSchema()
    try:
        register_schema.load(valid_data)
    except ValidationError as error_schema:
        error = error_schema.messages

    assert error == {
        "password": ["Your password must contain at least one lowercase letter."]
    }


def test_login_schema():
    valid_data = {"email": "jhondoe@test.com", "password": "Qwer.1234"}

    error = {}
    login_schema = serializers.LoginSchema()
    try:
        serializer = login_schema.load(valid_data)
    except ValidationError as error_schema:
        error = error_schema.messages

    assert serializer == valid_data
    assert error == {}


def test_empty_login_schema():
    valid_data = {}

    error = {}
    login_schema = serializers.LoginSchema()
    try:
        login_schema.load(valid_data)
    except ValidationError as error_schema:
        error = error_schema.messages

    assert error == {
        "email": ["Missing data for required field."],
        "password": ["Missing data for required field."],
    }


def test_invalid_email_login_schema():
    valid_data = {"email": "", "password": "Qwer.1234"}

    error = {}
    login_schema = serializers.LoginSchema()
    try:
        login_schema.load(valid_data)
    except ValidationError as error_schema:
        error = error_schema.messages

    assert error == {"email": ["Not a valid email address."]}


def test_email_verification_schema():
    valid_data = {
        "email": "jhondoe@test.com",
    }

    error = {}
    email_verification_schema = serializers.EmailVerificationSchema()
    try:
        serializer = email_verification_schema.load(valid_data)
    except ValidationError as error_schema:
        error = error_schema.messages

    assert serializer == valid_data
    assert error == {}


def test_empty_email_verification_schema():
    valid_data = {"email": ""}

    error = {}
    email_verification_schema = serializers.EmailVerificationSchema()
    try:
        email_verification_schema.load(valid_data)
    except ValidationError as error_schema:
        error = error_schema.messages

    assert error == {"email": ["Not a valid email address."]}


def test_invalid_email_verification_schema():
    valid_data = {}

    error = {}
    email_verification_schema = serializers.EmailVerificationSchema()
    try:
        email_verification_schema.load(valid_data)
    except ValidationError as error_schema:
        error = error_schema.messages

    assert error == {"email": ["Missing data for required field."]}


@pytest.mark.django_db
def test_user_token_schema():
    User = get_user_model()
    user = User.objects.create_user(email="normal@user.com", password="foo")
    valid_data = {"uidb36": utils.user_pk_to_url_str(user), "key": "jklsfdsfd546545sdf"}

    error = {}
    user_token_schema = serializers.UserTokenSchema()
    try:
        serializer = user_token_schema.load(valid_data)
    except ValidationError as error_schema:
        error = error_schema.messages

    assert serializer == valid_data
    assert error == {}


@pytest.mark.django_db
def test_invalid_uidb_user_token_schema():
    valid_data = {"uidb36": "jhfs", "key": "jklsfdsfd546545sdf"}

    error = {}
    user_token_schema = serializers.UserTokenSchema()
    try:
        user_token_schema.load(valid_data)
    except ValidationError as error_schema:
        error = error_schema.messages

    assert error == {"uidb36": ["The password reset token was invalid."]}


@pytest.mark.django_db
def test_invalid_user_token_schema():
    User = get_user_model()
    user = User.objects.create_user(email="normal@user.com", password="foo")
    valid_data = {"uidb36": utils.user_pk_to_url_str(user)}

    error = {}
    user_token_schema = serializers.UserTokenSchema()
    try:
        user_token_schema.load(valid_data)
    except ValidationError as error_schema:
        error = error_schema.messages

    assert error == {"key": ["The password reset token was invalid."]}


def test_password_schema():
    valid_data = {
        "password": "Qwer.1234",
    }

    error = {}
    password_schema = serializers.PasswordSchema()
    try:
        serializer = password_schema.load(valid_data)
    except ValidationError as error_schema:
        error = error_schema.messages

    assert serializer == valid_data
    assert error == {}


def test_invalid_password_schema():
    valid_data = {
        "password": "qwer.1234",
    }

    error = {}
    password_schema = serializers.PasswordSchema()
    try:
        password_schema.load(valid_data)
    except ValidationError as error_schema:
        error = error_schema.messages

    assert error == {
        "password": ["Your password must contain at least one uppercase letter."]
    }


def test_empty_password_schema():
    valid_data = {}

    error = {}
    password_schema = serializers.PasswordSchema()
    try:
        password_schema.load(valid_data)
    except ValidationError as error_schema:
        error = error_schema.messages

    assert error == {"password": ["Missing data for required field."]}
