from django.urls import path, re_path

from . import views

app_name = "accounts"

urlpatterns = [
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register_view, name="register"),
    # Confirmation Email
    path(
        "email-verification-sent/",
        views.email_verification_sent,
        name="email_verification_sent",
    ),
    re_path(
        r"^confirm-email/(?P<key>[-:\w]+)/$",
        views.confirm_email,
        name="confirm_email",
    ),
    # Password Reset
    path("password/reset", views.password_reset, name="reset_password"),
    re_path(
        r"^password/reset/key/(?P<uidb36>[0-9A-Za-z]+)-(?P<key>.+)/$",
        views.password_reset_from_key,
        name="reset_password_from_key",
    ),
    path("settings/change/password", views.change_password, name="change_password"),
    path(
        "resend-email-verification",
        views.resend_email_verification_api,
        name="resend_email_verification",
    ),
]
