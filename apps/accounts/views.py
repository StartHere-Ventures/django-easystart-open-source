import json

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.contrib.auth.tokens import default_token_generator
from django.http import JsonResponse
from django.shortcuts import redirect
from django.utils.translation import gettext_lazy as _
from django.views.decorators.http import require_http_methods
from inertia.share import share, share_flash
from inertia.views import render_inertia
from marshmallow import ValidationError

from apps.core import models as core_models
from utils.decorator import clean_message, json_format_required

from . import app_settings, models, serializers, tasks, utils

INTERNAL_RESET_URL_KEY = "set-password"
INTERNAL_RESET_SESSION_KEY = "_password_reset_key"


@require_http_methods(["GET", "POST"])
@clean_message
@json_format_required
def login_view(request):
    if request.user.is_authenticated:
        return redirect(app_settings.ACCOUNT_LOGIN_REDIRECT_URL)

    if request.method == "POST":
        login_schema = serializers.LoginSchema()
        try:
            data = login_schema.loads(request.body)
        except ValidationError as err:
            share_flash(request, error="Exists errors on form", errors=err.messages)
        else:
            user = authenticate(
                request, password=data.get("password"), email=data.get("email")
            )

            if (
                user
                and app_settings.EMAIL_VERIFICATION
                == app_settings.EmailVerificationMethod.MANDATORY
            ):
                email_address = models.EmailAddress.get_or_create(user)
                if not email_address.verified:
                    return redirect("accounts:email_verification_sent")

            if user is not None:
                login(request, user)
                share_flash(request)
                return redirect(app_settings.ACCOUNT_LOGIN_REDIRECT_URL)
            else:
                share_flash(
                    request,
                    error="Invalid email or password",
                )

    return render_inertia(request, "Login", {})


@require_http_methods(["GET"])
@clean_message
def logout_view(request):
    logout(request)
    return redirect(app_settings.ACCOUNT_LOGOUT_REDIRECT_URL)


@require_http_methods(["GET", "POST"])
@clean_message
@json_format_required
def register_view(request):
    global_settings = core_models.GlobalSettings.objects.first()
    if global_settings and not global_settings.active_registration:
        return redirect(app_settings.ACCOUNT_LOGIN_REDIRECT_URL)

    if request.method == "POST":
        data = json.loads(request.body)

        register_schema = serializers.RegisterSchema()
        try:
            data = register_schema.loads(request.body)
        except ValidationError as err:
            share_flash(request, error="Exists errors on form", errors=err.messages)
        else:
            try:
                user = core_models.CustomUser.create_user(
                    data.get("email"),
                    data.get("password"),
                    data.get("firstName"),
                    data.get("lastName"),
                )
            except ValueError as err:
                share_flash(
                    request,
                    error=str(err),
                )
            else:
                tasks.email_confirmation(request, user, True)
                if (
                    app_settings.EMAIL_VERIFICATION
                    == app_settings.EmailVerificationMethod.MANDATORY
                ):
                    return redirect(app_settings.ACCOUNT_SIGNIN_REDIRECT_URL)

                if app_settings.ACCOUNT_LOGIN_ON_SIGNIN:
                    user = authenticate(
                        request, password=data.get("password"), email=data.get("email")
                    )
                    if user is not None:
                        group = Group.objects.get(name="customer")
                        group.user_set.add(user)
                        login(request, user)
                        return redirect(app_settings.ACCOUNT_LOGIN_REDIRECT_URL)

                return redirect(app_settings.ACCOUNT_SIGNIN_REDIRECT_URL)
    props = {
        "paramsPasswordValidator": utils.get_params_password_validator(),
    }
    return render_inertia(request, "Register", props)


@require_http_methods(["GET", "POST"])
@clean_message
@json_format_required
def email_verification_sent(request):
    if request.method == "POST":
        email_schema = serializers.EmailVerificationSchema()
        try:
            data = email_schema.loads(request.body)
        except ValidationError as err:
            share_flash(request, error="Exists errors on form", errors=err.messages)
        else:
            user = core_models.CustomUser.objects.filter(email=data.get("email"))
            if user:
                can_send = models.EmailConfirmation.can_send_cooldown_period(
                    data.get("email")
                )
                if can_send:
                    tasks.email_confirmation(request, user.first(), True)
                    return redirect("accounts:login")
                else:
                    share_flash(
                        request,
                        error=_(
                            "Do you need wait {0} min to resend " "confirmation email"
                        ).format(int(app_settings.EMAIL_CONFIRMATION_COOLDOWN / 60)),
                    )
            else:
                share_flash(
                    request,
                    error="This email is not registered",
                )

    return render_inertia(request, "EmailVerificationSend", {})


@require_http_methods(["GET"])
@clean_message
def confirm_email(request, key):
    confirmation = models.EmailConfirmation.objects.filter(key=key)
    if not confirmation or confirmation.first().key_expired():
        return render_inertia(request, "ConfirmEmail", {})

    confirmation.first().confirm()
    if app_settings.LOGIN_ON_EMAIL_CONFIRMATION:
        login(request, confirmation.first().email_address.user)
        return redirect("accounts:login")

    return redirect(app_settings.EMAIL_CONFIRMATION_AUTHENTICATED_REDIRECT_URL)


@require_http_methods(["GET", "POST"])
@clean_message
@json_format_required
def password_reset(request):
    if request.method == "POST":
        email_schema = serializers.EmailVerificationSchema()
        try:
            data = email_schema.loads(request.body)
        except ValidationError as err:
            share_flash(request, error="Exists errors on form", errors=err.messages)
        else:
            user = core_models.CustomUser.objects.filter(email=data.get("email"))
            if user:
                tasks.email_password_reset(request, user.first())
                share(request, "message_other_view", True)
                share_flash(
                    request,
                    success="An email has been sent with instructions to reset your password",
                )
                return redirect("accounts:login")
            else:
                share_flash(
                    request,
                    error="This email is not registered",
                )

    return render_inertia(request, "PasswordReset", {})


@require_http_methods(["GET", "POST"])
@clean_message
@json_format_required
def password_reset_from_key(request, uidb36, key):
    if request.user.is_authenticated:
        logout(request)

    token_invalid = False
    token_schema = serializers.UserTokenSchema()
    try:
        token_schema.load(
            {
                "uidb36": str(uidb36),
                "key": str(key),
            }
        )
    except ValidationError:
        token_invalid = True
    else:
        reset_user = utils.get_user_from_uidb36(uidb36)
        token_generator = default_token_generator
        if not token_generator.check_token(reset_user, key):
            token_invalid = True

    if request.method == "POST" and not token_invalid:
        password_shema = serializers.PasswordSchema()
        try:
            data = password_shema.loads(request.body)
        except ValidationError as err:
            share_flash(request, error="Exists errors on form", errors=err.messages)
        else:
            reset_user.set_password(data.get("password"))
            reset_user.save()
            share_flash(
                request,
                success="Your password has been changed successfully",
            )
            share(request, "message_other_view", True)
            return redirect("accounts:login")

    props = {
        "uidb36": uidb36,
        "keyToken": key,
        "tokenInvalid": token_invalid,
        "paramsPasswordValidator": utils.get_params_password_validator(),
    }
    return render_inertia(request, "SetPasswordFromKey", props)


@require_http_methods(["GET", "POST"])
@login_required(login_url="/login", redirect_field_name=None)
@clean_message
def change_password(request):
    if request.method == "POST":
        tasks.email_password_reset(request, request.user)
        share_flash(
            request,
            success="An email has been sent with instructions to reset your password",
        )

    return render_inertia(request, "ChangePassword", {})


@require_http_methods(["GET"])
def resend_email_verification_api(request):
    if not request.user.is_authenticated:
        return JsonResponse(
            status=400, data={"status": "false", "message": "Login required"}
        )

    unconfirmed_email = models.EmailAddress.get_not_primary(request.user)
    can_send = models.EmailConfirmation.can_send_cooldown_period(unconfirmed_email)
    if can_send:
        tasks.email_confirmation(
            request, request.user, email=unconfirmed_email, signup=False, change=False
        )
        return JsonResponse(
            {
                "success": True,
                "timeResendEmail": models.EmailConfirmation.time_to_resend_email(
                    unconfirmed_email
                ),
            },
            safe=False,
        )
    else:
        return JsonResponse(
            {
                "error": _(
                    "Do you need wait {0} min to resend " "confirmation email"
                ).format(int(app_settings.EMAIL_CONFIRMATION_COOLDOWN / 60)),
            },
            safe=False,
        )
