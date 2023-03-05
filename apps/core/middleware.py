from datetime import datetime

from django.contrib.auth import logout
from django.shortcuts import redirect
from django.utils import translation
from django.utils.deprecation import MiddlewareMixin
from inertia.share import share, share_flash

from . import app_settings, models


class CorePropsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):

        if request.user.is_authenticated:
            try:
                user_profile = models.UserProfile.objects.get(user=request.user)
            except models.UserProfile.DoesNotExist:
                language = "en-us"
            else:
                language = user_profile.language
            translation.activate(language)
            share(request, "userLanguage", language)
        else:
            share(request, "userLanguage", None)

        global_settings = models.GlobalSettings.objects.first()
        if global_settings:
            settings = {
                "appName": global_settings.name_app
                if not global_settings.name_app == ""
                else "Django Easystart",
                "appLogo": global_settings.get_logo(),
                "timeExpiredSession": global_settings.session_expire_time,
                "activeRegistration": global_settings.active_registration,
            }
        else:
            settings = {
                "appName": "Django Easystart",
                "appLogo": "/static/img/logo.png",
                "timeExpiredSession": app_settings.SESSION_EXPIRE_TIME,
                "activeRegistration": True,
            }
        share(request, "globalSettings", settings)

        response = self.get_response(request)
        return response


class SessionIdleTimeout(MiddlewareMixin):
    """Middleware class to timeout a session after a specified time period."""

    def process_request(self, request):
        # Timeout is done only for authenticated logged in users.
        if request.user.is_authenticated:

            current = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
            idle_timeout = int(app_settings.SESSION_EXPIRE_TIME)

            global_settings = models.GlobalSettings.objects.first()
            if global_settings:
                idle_timeout = global_settings.session_expire_time

            # Timeout if idle time period is exceeded.
            if "last_activity" in request.session:
                last_activity = datetime.strptime(
                    request.session["last_activity"], "%Y-%m-%dT%H:%M:%S"
                )
                now = datetime.strptime(current, "%Y-%m-%dT%H:%M:%S")

                if (now - last_activity).seconds > idle_timeout * 60:
                    logout(request)
                    share_flash(
                        request,
                        error="Your session has been closed due to inactivity",
                        errors={
                            "error": "Your session has been closed due to inactivity"
                        },
                    )
                    share(request, "message_other_view", True)
                    return redirect("accounts:login")

                if request.accepts("text/html"):
                    request.session["last_activity"] = current
            else:
                request.session["last_activity"] = current

        return None
