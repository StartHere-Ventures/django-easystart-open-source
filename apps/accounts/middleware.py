from inertia import share

from apps.core.models import UserProfile

from . import app_settings, models


class AuthPropsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):

        if request.user.is_authenticated:
            try:
                email_address = models.EmailAddress.objects.get(
                    user=request.user, primary=True
                )
            except models.EmailAddress.DoesNotExist:
                verified = ""
            else:
                verified = email_address.verified

            try:
                user_profile = UserProfile.objects.get(user=request.user)
            except UserProfile.DoesNotExist:
                avatar = "/static/img/photo_default.png"
            else:
                avatar = user_profile.get_photo()

            share(
                request,
                auth={
                    "user": {
                        "id": request.user.id,
                        "firstName": request.user.first_name,
                        "lastName": request.user.last_name,
                        "email": request.user.email,
                        "groups": [
                            group["name"]
                            for group in request.user.groups.all().values("name")
                        ],
                        "permissions": list(request.user.get_group_permissions()),
                        "avatar": avatar,
                    },
                    "emailAddress": {
                        "verified": verified,
                        "emailMethod": app_settings.EMAIL_VERIFICATION,
                    },
                },
            )
        else:
            share(
                request,
                auth={
                    "user": {
                        "id": "",
                        "firstName": "",
                        "lastName": "",
                        "email": "",
                        "groups": [],
                        "permissions": [],
                        "avatar": None,
                    },
                    "emailAddress": {
                        "verified": "",
                        "emailMethod": app_settings.EMAIL_VERIFICATION,
                    },
                },
            )
        response = self.get_response(request)
        return response
