from django.urls import path

from . import views

app_name = "core"

urlpatterns = [
    path("", views.index, name="index"),
    path("index/settings", views.index_settings, name="index_settings"),
    path("settings", views.settings, name="settings"),
    path("settings/change/email", views.change_user_email, name="change_email"),
    path(
        "settings/cancel-change-email",
        views.cancel_change_email,
        name="cancel_change_email",
    ),
    path("settings/change/names", views.change_names, name="change_names"),
    path("settings/change/job", views.change_job_title, name="change_job_title"),
    path("settings/change/photo", views.change_photo, name="change_photo"),
    path("settings/remove/photo", views.remove_photo, name="remove_photo"),
    path("settings/change/language", views.change_language, name="change_language"),
    path("settings/change/country", views.change_country, name="change_country"),
    path(
        "settings/change/date-format",
        views.change_date_format,
        name="change_date_format",
    ),
    path("400", views.error_400, name="error_400"),
    path("403", views.error_403, name="error_403"),
    path("404", views.error_404, name="error_404"),
    path("500", views.error_500, name="error_500"),
]
