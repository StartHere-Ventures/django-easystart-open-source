from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import Group
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Q
from django.shortcuts import redirect
from django.views.decorators.http import require_http_methods
from inertia import render, share
from marshmallow import ValidationError

from apps.accounts import models as account_models
from apps.accounts import tasks as account_tasks
from apps.accounts import utils as account_utils
from apps.core import app_settings as core_settings
from apps.core import forms as core_forms
from apps.core import models as core_models
from apps.core import serialiazers as core_serializers
from apps.core import utils as core_utils
from apps.core.models import CustomUser
from utils.build_dict_language import get_dict_countries, get_dict_language
from utils.date_formats import DATE_FORMATS
from utils.decorator import clean_message, json_format_required
from utils.inertia import share_other_view

from . import forms, serializers


@require_http_methods(["GET"])
@login_required(login_url="/login", redirect_field_name=None)
@clean_message
def index(request):
    return render(
        request,
        "Index",
        {},
    )


@require_http_methods(["GET"])
@login_required(login_url="/login", redirect_field_name=None)
@permission_required("core.can_view_users", raise_exception=True)
@clean_message
def users_list(request):
    paginate_by = 10
    user_schema = serializers.UserSchema(many=True)
    users_obj = (
        CustomUser.objects.all()
        .exclude(is_superuser=True, is_staff=True)
        .order_by("id")
    )

    search = request.GET.get("search", None)
    if search is not None:
        users_obj = users_obj.filter(
            Q(email__icontains=search)
            | Q(first_name__icontains=search)
            | Q(last_name__icontains=search)
        )

    page = request.GET.get("page")
    count = users_obj.count()
    paginator = Paginator(users_obj, paginate_by)

    try:
        user_list = paginator.page(page)
    except PageNotAnInteger:
        user_list = paginator.page(1)
    except EmptyPage:
        user_list = paginator.page(paginator.num_pages)

    users = user_schema.dump(user_list)

    props = {
        "count": count,
        "paginateBy": paginate_by,
        "pages": paginator.num_pages,
        "currentPage": int(page) if page else 1,
        "users": users,
        "search": search,
    }
    return render(
        request,
        "Users",
        props,
    )


@require_http_methods(["GET"])
@login_required(login_url="/login", redirect_field_name=None)
@permission_required("core.can_view_user_detail", raise_exception=True)
@clean_message
def user_detail(request, user_id):
    user_schema = serializers.UserSchema()
    try:
        user_obj = CustomUser.objects.get(id=user_id)
    except CustomUser.DoesNotExist:
        share_other_view(request, error=True, errors="This user does not exist")
        share(request, message_other_view=True)
        return redirect("management:users")

    user = user_schema.dump(user_obj)

    props = {
        "user": user,
        "maxSizeFile": core_settings.MAX_SIZE_FILE,
        "availableLanguages": get_dict_language(),
        "availableCountries": get_dict_countries(),
        "availableGroups": core_utils.get_groups(),
        "availableDateFormats": DATE_FORMATS,
    }
    return render(
        request,
        "UserDetail",
        props,
    )


@require_http_methods(["GET"])
@login_required(login_url="/login", redirect_field_name=None)
@permission_required("core.can_edit_user", raise_exception=True)
@clean_message
def user_change_status(request, user_id):
    try:
        user = CustomUser.objects.get(id=user_id)
    except CustomUser.DoesNotExist:
        share_other_view(request, error=True, errors="This user does not exist")
        share(request, message_other_view=True)
        return redirect("management:users")
    else:
        user.is_active = not user.is_active
        user.save()
        share_other_view(
            request,
            success="Successful status change",
        )
        share(request, message_other_view=True)

    return redirect("management:user_detail", user_id=user.id)


@require_http_methods(["GET"])
@login_required(login_url="/login", redirect_field_name=None)
@permission_required("core.can_edit_user", raise_exception=True)
@clean_message
def user_reset_password(request, user_id):
    try:
        user = CustomUser.objects.get(id=user_id)
    except CustomUser.DoesNotExist:
        share_other_view(request, error=True, errors="This user does not exist")
        share(request, message_other_view=True)
        return redirect("management:users")
    else:
        account_tasks.email_password_reset(request, user)
        share(request, message_other_view=True)
        share_other_view(
            request,
            success="Email sent",
        )

    return redirect("management:user_detail", user_id=user.id)


@require_http_methods(["POST"])
@login_required(login_url="/login", redirect_field_name=None)
@permission_required("core.can_edit_user", raise_exception=True)
@clean_message
@json_format_required
def user_change_names(request, user_id):
    try:
        user = CustomUser.objects.get(id=user_id)
    except CustomUser.DoesNotExist:
        share_other_view(request, error=True, errors="This user does not exist")
        share(request, message_other_view=True)
        return redirect("management:users")

    names_schema = core_serializers.ProfileNamesSchema()
    try:
        data = names_schema.loads(request.body)
    except ValidationError as err:
        share_other_view(request, error="Exists errors on form", errors=err.messages)
    else:
        user.first_name = data.get("firstName")
        user.last_name = data.get("lastName")
        user.save()
        share_other_view(
            request,
            success="Successful name change",
        )
    share(request, message_other_view=True)

    return redirect("management:user_detail", user_id=user.id)


@require_http_methods(["POST"])
@login_required(login_url="/login", redirect_field_name=None)
@permission_required("core.can_edit_user", raise_exception=True)
@clean_message
def user_change_photo(request, user_id):
    try:
        user = CustomUser.objects.get(id=user_id)
    except CustomUser.DoesNotExist:
        share_other_view(request, error=True, errors="This user does not exist")
        share(request, message_other_view=True)
        return redirect("management:users")

    form = core_forms.ProfilePhotoForm(request.POST, request.FILES)
    if form.is_valid():
        user_profile = core_models.UserProfile.objects.get(user=user)
        user_profile.photo = form.cleaned_data["photo"]
        user_profile.save()
        share_other_view(
            request,
            success="Successful photo change",
        )
    else:
        share_other_view(request, error="Exists errors on form", errors=form.errors)

    share(request, message_other_view=True)

    return redirect("management:user_detail", user_id=user.id)


@require_http_methods(["GET"])
@login_required(login_url="/login", redirect_field_name=None)
@permission_required("core.can_edit_user", raise_exception=True)
@clean_message
def user_remove_photo(request, user_id):
    try:
        user = CustomUser.objects.get(id=user_id)
    except CustomUser.DoesNotExist:
        share_other_view(request, error=True, errors="This user does not exist")
        share(request, message_other_view=True)
        return redirect("management:users")

    user_profile = core_models.UserProfile.objects.get(user=user)
    user_profile.photo.delete()
    share_other_view(
        request,
        success="Photo successfully removed",
    )

    share(request, message_other_view=True)

    return redirect("management:user_detail", user_id=user.id)


@require_http_methods(["POST"])
@login_required(login_url="/login", redirect_field_name=None)
@permission_required("core.can_edit_user", raise_exception=True)
@clean_message
@json_format_required
def user_change_job_title(request, user_id):
    try:
        user = CustomUser.objects.get(id=user_id)
    except CustomUser.DoesNotExist:
        share_other_view(request, error=True, errors="This user does not exist")
        share(request, message_other_view=True)
        return redirect("management:users")

    job_schema = core_serializers.ProfileJobSchema()
    try:
        data = job_schema.loads(request.body)
    except ValidationError as err:
        share_other_view(request, error="Exists errors on form", errors=err.messages)
    else:
        user_profile = core_models.UserProfile.objects.get(user=user)
        user_profile.job_title = data.get("jobTitle")
        user_profile.save()
        share_other_view(
            request,
            success="Successful job title change",
        )
    share(request, message_other_view=True)

    return redirect("management:user_detail", user_id=user.id)


@require_http_methods(["POST"])
@login_required(login_url="/login", redirect_field_name=None)
@permission_required("core.can_edit_user", raise_exception=True)
@clean_message
@json_format_required
def change_language(request, user_id):
    try:
        user = CustomUser.objects.get(id=user_id)
    except CustomUser.DoesNotExist:
        share_other_view(request, error=True, errors="This user does not exist")
        share(request, message_other_view=True)
        return redirect("management:users")

    lang_schema = core_serializers.AccountLanguageSchema()
    try:
        data = lang_schema.loads(request.body)
    except ValidationError as err:
        share_other_view(request, error="Exists errors on form", errors=err.messages)
    else:
        user_profile = core_models.UserProfile.objects.get(user=user)
        user_profile.language = data.get("language")
        user_profile.save()
        share_other_view(
            request,
            success="Successful language change",
        )
    share(request, message_other_view=True)

    return redirect("management:user_detail", user_id=user.id)


@require_http_methods(["POST"])
@login_required(login_url="/login", redirect_field_name=None)
@permission_required("core.can_edit_user", raise_exception=True)
@clean_message
@json_format_required
def change_country(request, user_id):
    try:
        user = CustomUser.objects.get(id=user_id)
    except CustomUser.DoesNotExist:
        share_other_view(request, error=True, errors="This user does not exist")
        share(request, message_other_view=True)
        return redirect("management:users")

    country_schema = core_serializers.AccountCountrySchema()
    try:
        data = country_schema.loads(request.body)
    except ValidationError as err:
        share_other_view(request, error="Exists errors on form", errors=err.messages)
    else:
        user_profile = core_models.UserProfile.objects.get(user=user)
        user_profile.country = data.get("country")
        user_profile.save()
        share_other_view(
            request,
            success="Successful country change",
        )
    share(request, message_other_view=True)

    return redirect("management:user_detail", user_id=user.id)


@require_http_methods(["POST"])
@login_required(login_url="/login", redirect_field_name=None)
@permission_required("core.can_edit_user", raise_exception=True)
@clean_message
@json_format_required
def change_date_format(request, user_id):
    try:
        user = CustomUser.objects.get(id=user_id)
    except CustomUser.DoesNotExist:
        share_other_view(request, error=True, errors="This user does not exist")
        share(request, message_other_view=True)
        return redirect("management:users")

    date_schema = core_serializers.AccountDateFormatSchema()
    try:
        data = date_schema.loads(request.body)
    except ValidationError as err:
        share_other_view(request, error="Exists errors on form", errors=err.messages)
    else:
        user_profile = core_models.UserProfile.objects.get(user=user)
        user_profile.date_format = data.get("dateFormat")
        user_profile.save()
        share_other_view(
            request,
            success="Successful date format change",
        )
    share(request, message_other_view=True)

    return redirect("management:user_detail", user_id=user.id)


@require_http_methods(["POST"])
@login_required(login_url="/login", redirect_field_name=None)
@permission_required("core.can_edit_user", raise_exception=True)
@clean_message
@json_format_required
def change_user_groups(request, user_id):
    try:
        user = CustomUser.objects.get(id=user_id)
    except CustomUser.DoesNotExist:
        share_other_view(request, error=True, errors="This user does not exist")
        share(request, message_other_view=True)
        return redirect("management:users")

    group_schema = serializers.AccountUserGroupSchema()
    try:
        data = group_schema.loads(request.body)
    except ValidationError as err:
        share_other_view(request, error="Exists errors on form", errors=err.messages)
    else:
        for user_group in user.groups.all():
            user_group.user_set.remove(user)

        group = Group.objects.get(name=data.get("group"))
        group.user_set.add(user)

        share_other_view(
            request,
            success="Successful role change",
        )
    share(request, message_other_view=True)

    if user == request.user and data.get("group") == "customer":
        return redirect("accounts:login")

    return redirect("management:user_detail", user_id=user.id)


@require_http_methods(["GET", "POST"])
@login_required(login_url="/login", redirect_field_name=None)
@permission_required("core.can_create_user", raise_exception=True)
@clean_message
@json_format_required
def create_user(request):
    props = {
        "availableGroups": core_utils.get_groups(),
    }
    if request.method == "GET":
        return render(
            request,
            "UserCreate",
            props,
        )

    user_schema = serializers.CreateUserSchema()
    if request.method == "POST":
        try:
            data = user_schema.loads(request.body)
        except ValidationError as err:
            share(request, error="Exists errors on form", errors=err.messages)
            share(request, message_other_view=True)
            return render(
                request,
                "UserCreate",
                props,
            )
        else:
            password = account_utils.custom_password()
            try:
                user = core_models.CustomUser.create_user(
                    data.get("email"),
                    password,
                    data.get("firstName"),
                    data.get("lastName"),
                )
            except ValueError as err:
                share(
                    request,
                    error=str(err),
                )
                share(request, message_other_view=True)
                return render(
                    request,
                    "UserCreate",
                    props,
                )
            else:
                email_address = account_models.EmailAddress.get_or_create(
                    user, data.get("email")
                )
                email_address.primary = True
                email_address.verified = True
                email_address.save()
                account_tasks.email_password_reset(request, user)
                group = Group.objects.get(name=data.get("group"))
                group.user_set.add(user)

        return redirect("management:users")


@require_http_methods(["GET"])
@login_required(login_url="/login", redirect_field_name=None)
@permission_required("core.can_management_global_settings", raise_exception=True)
@clean_message
def global_settings_general(request):
    global_settings = core_models.GlobalSettings.objects.first()
    if not global_settings:
        global_settings = core_models.GlobalSettings()
        global_settings.save()

    props = {}
    return render(
        request,
        "SystemSettingsGeneral",
        props,
    )


@require_http_methods(["POST"])
@login_required(login_url="/login", redirect_field_name=None)
@permission_required("core.can_management_global_settings", raise_exception=True)
@clean_message
@json_format_required
def system_change_app_name(request):
    global_settings = core_models.GlobalSettings.objects.first()
    if not global_settings:
        share_other_view(request, error=True, errors="There is not a register of settings")
        share(request, message_other_view=True)
        return redirect("management:global_settings_general")

    app_schema = serializers.SystemAppNameSchema()
    try:
        data = app_schema.loads(request.body)
    except ValidationError as err:
        share_other_view(request, error="Exists errors on form", errors=err.messages)
    else:
        global_settings.name_app = data.get("appName")
        global_settings.save()
        share_other_view(
            request,
            success="Successful name change",
        )
    share(request, message_other_view=True)

    return redirect("management:global_settings_general")


@require_http_methods(["POST"])
@login_required(login_url="/login", redirect_field_name=None)
@permission_required("core.can_management_global_settings", raise_exception=True)
@clean_message
def system_change_app_logo(request):
    global_settings = core_models.GlobalSettings.objects.first()
    if not global_settings:
        share_other_view(request, error=True, errors="There is not a register of settings")
        share(request, message_other_view=True)
        return redirect("management:global_settings_general")

    form = forms.SystemAppLogoForm(request.POST, request.FILES)
    if form.is_valid():
        global_settings.logo_app = form.cleaned_data["logo"]
        global_settings.save()
        share_other_view(
            request,
            success="Successful logo change",
        )
    else:
        share_other_view(request, error="Exists errors on form", errors=form.errors)

    share(request, message_other_view=True)

    return redirect("management:global_settings_general")


@require_http_methods(["GET"])
@login_required(login_url="/login", redirect_field_name=None)
@permission_required("core.can_management_global_settings", raise_exception=True)
@clean_message
def system_remove_app_logo(request):
    global_settings = core_models.GlobalSettings.objects.first()
    if not global_settings:
        share_other_view(request, error=True, errors="There is not a register of settings")
        share(request, message_other_view=True)
        return redirect("management:global_settings_general")

    global_settings.logo_app.delete()
    share_other_view(
        request,
        success="Logo successfully removed",
    )

    share(request, message_other_view=True)

    return redirect("management:global_settings_general")


@require_http_methods(["GET"])
@login_required(login_url="/login", redirect_field_name=None)
@permission_required("core.can_management_global_settings", raise_exception=True)
@clean_message
def global_settings_security(request):
    global_settings = core_models.GlobalSettings.objects.first()
    if not global_settings:
        global_settings = core_models.GlobalSettings()
        global_settings.save()

    props = {"auditInstalled": core_utils.is_audit_installed()}
    return render(
        request,
        "SystemSettingsSecurity",
        props,
    )


@require_http_methods(["POST"])
@login_required(login_url="/login", redirect_field_name=None)
@permission_required("core.can_management_global_settings", raise_exception=True)
@clean_message
@json_format_required
def system_change_session_expire_time(request):
    global_settings = core_models.GlobalSettings.objects.first()
    if not global_settings:
        share_other_view(request, error=True, errors="There is not a register of settings")
        share(request, message_other_view=True)
        return redirect("management:global_settings_security")

    app_schema = serializers.SystemExpireTimeSchema()
    try:
        data = app_schema.loads(request.body)
    except ValidationError as err:
        share_other_view(request, error="Exists errors on form", errors=err.messages)
    else:
        global_settings.session_expire_time = data.get("sessionExpireTime")
        global_settings.save()
        share_other_view(
            request,
            success="Successful session expiration time change",
        )
    share(request, message_other_view=True)

    return redirect("management:global_settings_security")


@require_http_methods(["GET", "POST"])
@login_required(login_url="/login", redirect_field_name=None)
@permission_required("core.can_management_global_settings", raise_exception=True)
@clean_message
@json_format_required
def global_settings_scripts(request):
    global_settings = core_models.GlobalSettings.objects.first()
    if not global_settings:
        global_settings = core_models.GlobalSettings()
        global_settings.save()

    if request.method == "POST":
        script_schema = serializers.GlobalSettingsScripts()
        try:
            data = script_schema.loads(request.body)
        except ValidationError as err:
            share(request, error="Exists errors on form", errors=err.messages)
        else:
            global_settings.header_scripts = data.get("header")
            global_settings.footer_scripts = data.get("footer")
            global_settings.body_scripts = data.get("body")
            global_settings.save()

            share(
                request,
                success="Scripts saved successfully",
            )

    props = {
        "header": global_settings.header_scripts
        if global_settings.header_scripts is not None
        else "",
        "footer": global_settings.footer_scripts
        if global_settings.footer_scripts is not None
        else "",
        "body": global_settings.body_scripts
        if global_settings.body_scripts is not None
        else "",
    }

    return render(
        request,
        "SystemSettingsScripts",
        props,
    )


@require_http_methods(["GET"])
@login_required(login_url="/login", redirect_field_name=None)
@permission_required("core.can_management_global_settings", raise_exception=True)
@clean_message
def system_active_registration(request):
    global_settings = core_models.GlobalSettings.objects.first()
    if not global_settings:
        share_other_view(request, error=True, errors="There is not a register of settings")
        share(request, message_other_view=True)
        return redirect("management:global_settings_general")

    global_settings.active_registration = not global_settings.active_registration
    global_settings.save()

    msg = "User registration active"
    if not global_settings.active_registration:
        msg = "User registration deactive"
    share_other_view(
        request,
        success=msg,
    )
    share(request, message_other_view=True)

    return redirect("management:global_settings_general")
