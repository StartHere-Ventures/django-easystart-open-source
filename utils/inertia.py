def share_other_view(request, success=False, error=False, errors=False):
    if success:
        request.session["success"] = success
    if error:
        request.session["error"] = error
    if errors:
        request.session["errors"] = errors

    request.session["message_other_view"] = True
    if not success and not error and not errors:
        request.session["message_other_view"] = False
