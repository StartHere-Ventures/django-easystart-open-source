import json
from functools import wraps

from django.contrib.auth.decorators import user_passes_test
from django.http import JsonResponse
from inertia.share import share, share_flash


def clean_message(func):
    """
    Clean share sessions if there not message from other view
    """

    @wraps(func)
    def wrapper(request, *args, **kwargs):
        if not request.session["share"].get("message_other_view", False):
            share_flash(request, error=False, success=False)
            share(request, "errors", {})
        share(request, "message_other_view", False)

        return func(request, *args, **kwargs)

    return wrapper


def group_required(*group_names):
    """Requires user membership in at least one of the groups passed in."""

    def in_groups(u):
        if u.is_authenticated:
            if bool(u.groups.filter(name__in=group_names)) | u.is_superuser:
                return True
        return False

    return user_passes_test(in_groups, login_url="/403", redirect_field_name=None)


def json_format_required(func, method="POST"):
    """
    Validate json format in request data
    """

    @wraps(func)
    def wrapper(request, *args, **kwargs):
        if request.method == method:
            try:
                json.loads(request.body)
            except json.decoder.JSONDecodeError:
                return JsonResponse(
                    {"error": True, "message": "Json format required in data"},
                    status=400,
                    safe=False,
                )

        return func(request, *args, **kwargs)

    return wrapper
