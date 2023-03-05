def get_ip(request):
    ip = request.META["REMOTE_ADDR"]
    if request.META.get("HTTP_X_FORWARDED_FOR"):
        ip = request.META.get("HTTP_X_FORWARDED_FOR").split(",")[0]

    return ip


def get_device(request):
    return "{0} {1} ({2})".format(
        request.user_agent.browser.family,
        request.user_agent.browser.version_string,
        request.user_agent.os.family,
    )
