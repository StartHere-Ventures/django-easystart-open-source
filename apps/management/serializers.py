from marshmallow import Schema, ValidationError, fields, validate

from apps.core import models, serialiazers, utils


def get_user_profile(user):
    try:
        user_profile = models.UserProfile.objects.get(user=user)
    except models.UserProfile.DoesNotExist:
        user_profile = models.UserProfile(user=user)
        user_profile.save()
    else:
        return serialiazers.ProfileSchema().dump(user_profile)


class GroupsSchema(Schema):
    name = fields.Str()


class UserSchema(Schema):
    email = fields.Email()
    first_name = fields.Str(data_key="firstName")
    last_name = fields.Str(data_key="lastName")
    is_active = fields.Boolean(data_key="isActive")
    user_id = fields.Function(lambda o: o.id)
    groups = fields.Function(lambda o: GroupsSchema(many=True).dump(o.groups.all()))
    profile = fields.Function(lambda o: get_user_profile(o))


def user_group_validation(value):
    groups = utils.get_groups()
    try:
        groups[value]
    except KeyError:
        raise ValidationError("Invalid user group.")


class CreateUserSchema(Schema):
    firstName = fields.Str(required=True)
    lastName = fields.Str(required=True)
    email = fields.Email(required=True)
    group = fields.Str(required=True, validate=user_group_validation)


class SystemAppNameSchema(Schema):
    appName = fields.Str(required=True, validate=validate.Length(min=1))


class SystemExpireTimeSchema(Schema):
    sessionExpireTime = fields.Integer(required=True)


class AccountUserGroupSchema(Schema):
    group = fields.Str(required=True, validate=user_group_validation)


class GlobalSettingsScripts(Schema):
    header = fields.Str(required=True)
    body = fields.Str(required=True)
    footer = fields.Str(required=True)
