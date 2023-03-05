from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError as ValidError
from django_countries import countries
from marshmallow import Schema, ValidationError, fields, validate

from apps.accounts import models as accounts_models
from utils.build_dict_language import get_dict_language
from utils.date_formats import DATE_FORMATS


class ProfileSchema(Schema):
    job_title = fields.Str(required=True)
    date_format = fields.Method("get_date_format")
    country = fields.Method("get_country")
    language = fields.Str(required=True)
    photo = fields.Method("get_photo")

    def get_photo(self, obj):
        return obj.get_photo()

    def get_country(self, obj):
        if obj.country:
            return obj.country.code
        return None

    def get_date_format(self, obj):
        return obj.date_format.upper()


def user_email_validation(value):
    if bool(accounts_models.EmailAddress.objects.filter(email=value, primary=True)):
        raise ValidationError("This email already verified")


def password_validation(value):
    try:
        validate_password(value)
    except ValidError as error:
        raise ValidationError(error)


class ProfileEmailSchema(Schema):
    password = fields.Str(required=True, validate=password_validation)
    email = fields.Email(required=True, validate=user_email_validation)


class ProfileNamesSchema(Schema):
    firstName = fields.Str(required=True, validate=validate.Length(min=1))
    lastName = fields.Str(required=True, validate=validate.Length(min=1))


class ProfileJobSchema(Schema):
    jobTitle = fields.Str(required=True, validate=validate.Length(min=1))


def language_validation(value):
    lang = get_dict_language()
    try:
        lang[value]
    except KeyError:
        raise ValidationError("Invalid language")


class AccountLanguageSchema(Schema):
    language = fields.Str(required=True, validate=language_validation)


def country_validation(value):
    try:
        dict(countries)[value.upper()]
    except KeyError:
        raise ValidationError("Invalid country")


class AccountCountrySchema(Schema):
    country = fields.Str(required=True, validate=country_validation)


def date_format_validation(value):
    try:
        DATE_FORMATS[value.upper()]
    except KeyError:
        raise ValidationError("Invalid date format")


class AccountDateFormatSchema(Schema):
    dateFormat = fields.Str(required=True, validate=date_format_validation)
