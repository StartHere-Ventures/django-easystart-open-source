from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError as ValidError
from marshmallow import Schema, ValidationError, fields

from . import utils


def password_validation(value):
    try:
        validate_password(value)
    except ValidError as error:
        raise ValidationError(error)


class RegisterSchema(Schema):
    firstName = fields.Str(required=True)
    lastName = fields.Str(required=True)
    email = fields.Email(required=True)
    password = fields.Str(required=True, validate=password_validation)


class LoginSchema(Schema):
    email = fields.Email(required=True)
    password = fields.Str(required=True)


class EmailVerificationSchema(Schema):
    email = fields.Email(required=True)


def uidb36_validator(value):
    try:
        utils.get_user_from_uidb36(value)
    except ValueError:
        raise ValidationError("The password reset token was invalid.")


class UserTokenSchema(Schema):
    uidb36 = fields.Str(validate=uidb36_validator)
    key = fields.Str(
        required=True,
        error_messages={"required": "The password reset token was invalid."},
    )


class PasswordSchema(Schema):
    password = fields.Str(required=True, validate=password_validation)
