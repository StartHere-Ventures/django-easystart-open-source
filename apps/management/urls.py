from django.urls import path, re_path

from apps.accounts import views as accounts_views
from apps.core import views as core_views

from . import views

app_name = "management"

urlpatterns = [
    path("", views.index, name="index"),
    path("users", views.users_list, name="users"),
    re_path(
        r"^user/(?P<user_id>[-:\w]+)/$",
        views.user_detail,
        name="user_detail",
    ),
    # User Profile Edit
    re_path(
        r"^user/(?P<user_id>[-:\w]+)/change/names$",
        views.user_change_names,
        name="user_change_names",
    ),
    re_path(
        r"^user/(?P<user_id>[-:\w]+)/change/job$",
        views.user_change_job_title,
        name="user_change_job_title",
    ),
    re_path(
        r"^user/(?P<user_id>[-:\w]+)/change/photo$",
        views.user_change_photo,
        name="user_change_photo",
    ),
    re_path(
        r"^user/(?P<user_id>[-:\w]+)/remove/photo$",
        views.user_remove_photo,
        name="user_remove_photo",
    ),
    # User Account
    re_path(
        r"^user/(?P<user_id>[-:\w]+)/change/language$",
        views.change_language,
        name="user_change_language",
    ),
    re_path(
        r"^user/(?P<user_id>[-:\w]+)/change/country$",
        views.change_country,
        name="user_change_country",
    ),
    re_path(
        r"^user/(?P<user_id>[-:\w]+)/change/date-format$",
        views.change_date_format,
        name="user_change_date_format",
    ),
    re_path(
        r"^user/(?P<user_id>[-:\w]+)/change/group$",
        views.change_user_groups,
        name="change_user_groups",
    ),
    # User Security
    re_path(
        r"^user/(?P<user_id>[-:\w]+)/change-status$",
        views.user_change_status,
        name="user_change_status",
    ),
    re_path(
        r"^user/(?P<user_id>[-:\w]+)/reset-password$",
        views.user_reset_password,
        name="user_reset_password",
    ),
    path("users/create", views.create_user, name="user_create"),
    # Settings
    path("settings", core_views.settings, name="settings"),
    path(
        "settings/change/password",
        accounts_views.change_password,
        name="change_password",
    ),
    path(
        "settings/global/general",
        views.global_settings_general,
        name="global_settings_general",
    ),
    path(
        "settings/system/change/app-name",
        views.system_change_app_name,
        name="system_change_app_name",
    ),
    path(
        "settings/system/change/app-logo",
        views.system_change_app_logo,
        name="system_change_app_logo",
    ),
    path(
        "settings/system/remove/app-logo",
        views.system_remove_app_logo,
        name="system_remove_app_logo",
    ),
    path(
        "settings/global/security",
        views.global_settings_security,
        name="global_settings_security",
    ),
    path(
        "settings/global/security/change/session-expire-time",
        views.system_change_session_expire_time,
        name="system_change_session_expire_time",
    ),
    path(
        "settings/global/scripts",
        views.global_settings_scripts,
        name="global_settings_scripts",
    ),
    path(
        "settings/global/active/registration",
        views.system_active_registration,
        name="system_active_registration",
    ),
]
