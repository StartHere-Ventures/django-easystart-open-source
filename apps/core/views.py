import json

from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.utils.translation import gettext_lazy as _
from django.views.decorators.http import require_http_methods
from inertia import render, share
from marshmallow import ValidationError

from apps.accounts import app_settings as account_app_settings
from apps.accounts import models as accounts_model
from apps.accounts import tasks as account_tasks
from utils.build_dict_language import get_dict_countries, get_dict_language
from utils.date_formats import DATE_FORMATS
from utils.decorator import clean_message, json_format_required
from utils.inertia import share_other_view

from . import app_settings, forms, models, serialiazers


@require_http_methods(["GET"])
@login_required(login_url="/login", redirect_field_name=None)
@clean_message
def index(request):
    if bool(request.user.groups.filter(name="customer")):
        return render(
            request,
            "Index",
            {},
        )

    return redirect("management:index")


# Settings
@require_http_methods(["GET"])
def index_settings(request):
    if bool(request.user.groups.filter(name="management")):
        return redirect("management:settings")

    return redirect("core:settings")


@require_http_methods(["GET"])
@login_required(login_url="/login", redirect_field_name=None)
@clean_message
def settings(request):
    try:
        user_profile = models.UserProfile.objects.get(user=request.user)
    except models.UserProfile.DoesNotExist:
        user_profile = models.UserProfile(user=request.user)
        user_profile.save()

    profile_schema = serialiazers.ProfileSchema()
    profile = profile_schema.dump(user_profile)

    props = {
        "unconfirmedEmail": accounts_model.EmailAddress.get_not_primary(request.user),
        "userProfile": profile,
        "maxSizeFile": app_settings.MAX_SIZE_FILE,
        "availableLanguages": get_dict_language(),
        "availableCountries": get_dict_countries(),
        "availableDateFormats": DATE_FORMATS,
        "timeResendEmail": accounts_model.EmailConfirmation.time_to_resend_email(
            accounts_model.EmailAddress.get_not_primary(request.user)
        ),
    }

    return render(
        request,
        "SettingsIndex",
        props,
    )


@require_http_methods(["POST"])
@login_required(login_url="/login", redirect_field_name=None)
@clean_message
@json_format_required
def change_user_email(request):
    if request.method == "POST":
        email_schema = serialiazers.ProfileEmailSchema()
        try:
            data = email_schema.loads(request.body)
        except ValidationError as err:
            share_other_view(request, error="Exists errors on form", errors=err.messages)
        else:
            user = authenticate(
                request, password=data.get("password"), email=request.user.email
            )
            if not user:
                share_other_view(
                    request,
                    error="Exists errors on form",
                    errors={"password": ["Wrong password"]},
                )
                share(request, message_other_view=True)
                return redirect("core:index_settings")

            if bool(
                models.CustomUser.objects.filter(email=data.get("email")).exclude(
                    id=request.user.id
                )
            ):
                share_other_view(
                    request,
                    error="Exists errors on form",
                    errors={"email": ["This email already registered"]},
                )
                share(request, message_other_view=True)
                return redirect("core:index_settings")

            can_send = accounts_model.EmailConfirmation.can_send_cooldown_period(
                data.get("email")
            )
            if not can_send:
                share_other_view(
                    request,
                    error=True,
                    errors={
                        "email": [
                            _(
                                "Do you need wait {0} min to resend confirmation email"
                            ).format(
                                int(
                                    account_app_settings.EMAIL_CONFIRMATION_COOLDOWN
                                    / 60
                                )
                            )
                        ]
                    },
                )
            else:
                account_tasks.email_confirmation(
                    request,
                    request.user,
                    signup=False,
                    email=data.get("email"),
                    change=True,
                )
                share_other_view(
                    request,
                    success="A confirmation email has been send",
                )
        share(request, message_other_view=True)

    return redirect("core:index_settings")


@require_http_methods(["POST"])
@login_required(login_url="/login", redirect_field_name=None)
@clean_message
@json_format_required
def cancel_change_email(request):
    if request.method == "POST":
        data = json.loads(request.body)
        email = data.get("email")
        if not request.user.email == email:
            email_address = accounts_model.EmailAddress.objects.filter(email=email)
            if email_address:
                email_address.first().delete()
                share_other_view(
                    request,
                    success="Change email canceled",
                )
                email_address = accounts_model.EmailAddress.get_or_create(request.user)
                accounts_model.EmailConfirmation.can_send_cooldown_period(
                    request.user.email
                )
                share(request, message_other_view=True)

    return redirect("core:index_settings")


@require_http_methods(["POST"])
@login_required(login_url="/login", redirect_field_name=None)
@clean_message
@json_format_required
def change_names(request):
    if request.method == "POST":
        names_schema = serialiazers.ProfileNamesSchema()
        try:
            data = names_schema.loads(request.body)
        except ValidationError as err:
            share_other_view(request, error="Exists errors on form", errors=err.messages)
        else:
            request.user.first_name = data.get("firstName")
            request.user.last_name = data.get("lastName")
            request.user.save()
            share_other_view(
                request,
                success="Successful name change",
            )
        share(request, message_other_view=True)

    return redirect("core:index_settings")


@require_http_methods(["POST"])
@login_required(login_url="/login", redirect_field_name=None)
@clean_message
@json_format_required
def change_job_title(request):
    if request.method == "POST":
        job_schema = serialiazers.ProfileJobSchema()
        try:
            data = job_schema.loads(request.body)
        except ValidationError as err:
            share_other_view(request, error="Exists errors on form", errors=err.messages)
        else:
            user_profile = models.UserProfile.objects.get(user=request.user)
            user_profile.job_title = data.get("jobTitle")
            user_profile.save()
            share_other_view(
                request,
                success="Successful job title change",
            )
        share(request, message_other_view=True)

    return redirect("core:index_settings")


@require_http_methods(["POST"])
@login_required(login_url="/login", redirect_field_name=None)
@clean_message
def change_photo(request):
    if request.method == "POST":
        form = forms.ProfilePhotoForm(request.POST, request.FILES)
        if form.is_valid():
            user_profile = models.UserProfile.objects.get(user=request.user)
            user_profile.photo = form.cleaned_data["photo"]
            user_profile.save()
            share_other_view(
                request,
                success="Successful photo change",
            )
        else:
            share_other_view(request, error="Exists errors on form", errors=form.errors)

        share(request, message_other_view=True)

    return redirect("core:index_settings")


@require_http_methods(["GET", "POST"])
@login_required(login_url="/login", redirect_field_name=None)
@clean_message
def remove_photo(request):
    user_profile = models.UserProfile.objects.get(user=request.user)
    user_profile.photo.delete()
    share_other_view(
        request,
        success="Photo successfully removed",
    )

    share(request, message_other_view=True)

    return redirect("core:index_settings")


@require_http_methods(["POST"])
@login_required(login_url="/login", redirect_field_name=None)
@clean_message
@json_format_required
def change_language(request):
    if request.method == "POST":
        lang_schema = serialiazers.AccountLanguageSchema()
        try:
            data = lang_schema.loads(request.body)
        except ValidationError as err:
            share_other_view(request, error="Exists errors on form", errors=err.messages)
        else:
            user_profile = models.UserProfile.objects.get(user=request.user)
            user_profile.language = data.get("language")
            user_profile.save()
            share_other_view(
                request,
                success="Successful language change",
            )
        share(request, message_other_view=True)

    return redirect("core:index_settings")


@require_http_methods(["POST"])
@login_required(login_url="/login", redirect_field_name=None)
@clean_message
@json_format_required
def change_country(request):
    if request.method == "POST":
        country_schema = serialiazers.AccountCountrySchema()
        try:
            data = country_schema.loads(request.body)
        except ValidationError as err:
            share_other_view(request, error="Exists errors on form", errors=err.messages)
        else:
            user_profile = models.UserProfile.objects.get(user=request.user)
            user_profile.country = data.get("country")
            user_profile.save()
            share_other_view(
                request,
                success="Successful country change",
            )
        share(request, message_other_view=True)

    return redirect("core:index_settings")


@require_http_methods(["POST"])
@login_required(login_url="/login", redirect_field_name=None)
@clean_message
@json_format_required
def change_date_format(request):
    if request.method == "POST":
        date_schema = serialiazers.AccountDateFormatSchema()
        try:
            data = date_schema.loads(request.body)
        except ValidationError as err:
            share_other_view(request, error="Exists errors on form", errors=err.messages)
        else:
            user_profile = models.UserProfile.objects.get(user=request.user)
            user_profile.date_format = data.get("dateFormat")
            user_profile.save()
            share_other_view(
                request,
                success="Successful date format change",
            )
        share(request, message_other_view=True)

    return redirect("core:index_settings")


# Page errors
@require_http_methods(["GET"])
def error_404(request, exception=None):
    # Try to get an "interesting" exception message, if any (and not the ugly
    # Resolver404 dictionary)
    try:
        exception.args[0]
    except (AttributeError, IndexError):
        pass

    return render(
        request,
        "404Error",
        {},
    )


@require_http_methods(["GET"])
def error_400(request, exception=None):
    return render(
        request,
        "400Error",
        {},
    )


@require_http_methods(["GET"])
def error_403(request, exception=None):
    return render(
        request,
        "403Error",
        {},
    )


@require_http_methods(["GET"])
def error_500(request):
    return render(
        request,
        "500Error",
        {},
    )
