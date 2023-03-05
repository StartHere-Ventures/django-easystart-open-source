import pytest
from marshmallow import ValidationError

from apps.core import models, serialiazers


@pytest.mark.django_db
def test_profile_schema(create_user):
    user = create_user()
    user_profile = models.UserProfile(user=user)
    user_profile.save()

    schema = serialiazers.ProfileSchema()
    profile = schema.dump(user_profile)
    assert isinstance(profile, type({}))
    assert "job_title" in profile
    assert "date_format" in profile
    assert "country" in profile
    assert "language" in profile
    assert "photo" in profile


@pytest.mark.django_db
def test_profile_email_schema():
    valid_data = {"password": "Qwer.1234", "email": "jhondoe@test.com"}

    error = {}
    profile_email_schema = serialiazers.ProfileEmailSchema()
    try:
        serializer = profile_email_schema.load(valid_data)
    except ValidationError as error_schema:
        error = error_schema.messages

    assert serializer == valid_data
    assert error == {}


@pytest.mark.django_db
def test_invalid_profile_email_schema():
    valid_data = {}

    error = {}
    profile_email_schema = serialiazers.ProfileEmailSchema()
    try:
        profile_email_schema.load(valid_data)
    except ValidationError as error_schema:
        error = error_schema.messages

    assert error == {
        "password": ["Missing data for required field."],
        "email": ["Missing data for required field."],
    }


@pytest.mark.django_db
def test_empty_email_profile_email_schema():
    valid_data = {"password": "Qwer.1234", "email": ""}

    error = {}
    profile_email_schema = serialiazers.ProfileEmailSchema()
    try:
        profile_email_schema.load(valid_data)
    except ValidationError as error_schema:
        error = error_schema.messages

    assert error == {"email": ["Not a valid email address."]}


@pytest.mark.django_db
def test_invalid_password_profile_email_schema():
    valid_data = {"password": "QWER.1234", "email": "jhondoe@test.com"}

    error = {}
    profile_email_schema = serialiazers.ProfileEmailSchema()
    try:
        profile_email_schema.load(valid_data)
    except ValidationError as error_schema:
        error = error_schema.messages

    assert error == {
        "password": ["Your password must contain at least one lowercase letter."]
    }


def test_profile_names():
    valid_data = {"firstName": "Jhon", "lastName": "Doe"}

    error = {}
    profile_name_schema = serialiazers.ProfileNamesSchema()
    try:
        serializer = profile_name_schema.load(valid_data)
    except ValidationError as error_schema:
        error = error_schema.messages

    assert serializer == valid_data
    assert error == {}


def test_invalid_profile_names():
    valid_data = {}

    error = {}
    profile_name_schema = serialiazers.ProfileNamesSchema()
    try:
        profile_name_schema.load(valid_data)
    except ValidationError as error_schema:
        error = error_schema.messages

    assert (
        error
        == error
        == {
            "firstName": ["Missing data for required field."],
            "lastName": ["Missing data for required field."],
        }
    )


def test_empty_names_profile_names():
    valid_data = {"firstName": "", "lastName": ""}

    error = {}
    profile_name_schema = serialiazers.ProfileNamesSchema()
    try:
        profile_name_schema.load(valid_data)
    except ValidationError as error_schema:
        error = error_schema.messages

    assert error == {
        "firstName": ["Shorter than minimum length 1."],
        "lastName": ["Shorter than minimum length 1."],
    }


def test_profile_jobs():
    valid_data = {
        "jobTitle": "Developer",
    }

    error = {}
    profile_jobs_schema = serialiazers.ProfileJobSchema()
    try:
        serializer = profile_jobs_schema.load(valid_data)
    except ValidationError as error_schema:
        error = error_schema.messages

    assert serializer == valid_data
    assert error == {}


def test_invalid_profile_jobs():
    valid_data = {}

    error = {}
    profile_jobs_schema = serialiazers.ProfileJobSchema()
    try:
        profile_jobs_schema.load(valid_data)
    except ValidationError as error_schema:
        error = error_schema.messages

    assert error == {"jobTitle": ["Missing data for required field."]}


def test_empty_names_profile_jobs():
    valid_data = {
        "jobTitle": "",
    }

    error = {}
    profile_jobs_schema = serialiazers.ProfileJobSchema()
    try:
        profile_jobs_schema.load(valid_data)
    except ValidationError as error_schema:
        error = error_schema.messages

    assert error == {"jobTitle": ["Shorter than minimum length 1."]}


def test_account_language():
    valid_data = {
        "language": "en-us",
    }

    error = {}
    account_language_schema = serialiazers.AccountLanguageSchema()
    try:
        serializer = account_language_schema.load(valid_data)
    except ValidationError as error_schema:
        error = error_schema.messages

    assert serializer == valid_data
    assert error == {}


def test_invalid_account_language():
    valid_data = {}

    error = {}
    account_language_schema = serialiazers.AccountLanguageSchema()
    try:
        account_language_schema.load(valid_data)
    except ValidationError as error_schema:
        error = error_schema.messages

    assert error == {"language": ["Missing data for required field."]}


def test_empty_lang_account_language():
    valid_data = {
        "language": "",
    }

    error = {}
    account_language_schema = serialiazers.AccountLanguageSchema()
    try:
        account_language_schema.load(valid_data)
    except ValidationError as error_schema:
        error = error_schema.messages

    assert error == {"language": ["Invalid language"]}


def test_account_country():
    valid_data = {
        "country": "ES",
    }

    error = {}
    account_country_schema = serialiazers.AccountCountrySchema()
    try:
        serializer = account_country_schema.load(valid_data)
    except ValidationError as error_schema:
        error = error_schema.messages

    assert serializer == valid_data
    assert error == {}


def test_invalid_account_country():
    valid_data = {}

    error = {}
    account_country_schema = serialiazers.AccountCountrySchema()
    try:
        account_country_schema.load(valid_data)
    except ValidationError as error_schema:
        error = error_schema.messages

    assert error == {"country": ["Missing data for required field."]}


def test_empty_country_account_country():
    valid_data = {
        "country": "",
    }

    error = {}
    account_country_schema = serialiazers.AccountCountrySchema()
    try:
        account_country_schema.load(valid_data)
    except ValidationError as error_schema:
        error = error_schema.messages

    assert error == {"country": ["Invalid country"]}


def test_account_date_format():
    valid_data = {
        "dateFormat": "dd-mm-yyyy",
    }

    error = {}
    account_date_format_schema = serialiazers.AccountDateFormatSchema()
    try:
        serializer = account_date_format_schema.load(valid_data)
    except ValidationError as error_schema:
        error = error_schema.messages

    assert serializer == valid_data
    assert error == {}


def test_invalid_account_date_format():
    valid_data = {}

    error = {}
    account_date_format_schema = serialiazers.AccountDateFormatSchema()
    try:
        account_date_format_schema.load(valid_data)
    except ValidationError as error_schema:
        error = error_schema.messages

    assert error == {"dateFormat": ["Missing data for required field."]}


def test_empty_date_account_date_format():
    valid_data = {
        "dateFormat": "",
    }

    error = {}
    account_date_format_schema = serialiazers.AccountDateFormatSchema()
    try:
        account_date_format_schema.load(valid_data)
    except ValidationError as error_schema:
        error = error_schema.messages

    assert error == {"dateFormat": ["Invalid date format"]}
