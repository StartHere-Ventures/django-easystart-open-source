window.routes = {"core:index": "/", "core:index_settings": "/index/settings", "core:settings": "/settings", "core:change_email": "/settings/change/email", "core:cancel_change_email": "/settings/cancel-change-email", "core:change_names": "/settings/change/names", "core:change_job_title": "/settings/change/job", "core:change_photo": "/settings/change/photo", "core:remove_photo": "/settings/remove/photo", "core:change_language": "/settings/change/language", "core:change_country": "/settings/change/country", "core:change_date_format": "/settings/change/date-format", "core:error_400": "/400", "core:error_403": "/403", "core:error_404": "/404", "core:error_500": "/500", "accounts:login": "/login", "accounts:logout": "/logout", "accounts:register": "/register", "accounts:email_verification_sent": "/email-verification-sent/", "accounts:confirm_email": "/confirm-email/<key>/", "accounts:reset_password": "/password/reset", "accounts:reset_password_from_key": "/password/reset/key/<uidb36>-<key>/", "accounts:change_password": "/settings/change/password", "accounts:resend_email_verification": "/resend-email-verification", "management:index": "/manage/", "management:users": "/manage/users", "management:user_detail": "/manage/user/<user_id>/", "management:user_change_names": "/manage/user/<user_id>/change/names", "management:user_change_job_title": "/manage/user/<user_id>/change/job", "management:user_change_photo": "/manage/user/<user_id>/change/photo", "management:user_remove_photo": "/manage/user/<user_id>/remove/photo", "management:user_change_language": "/manage/user/<user_id>/change/language", "management:user_change_country": "/manage/user/<user_id>/change/country", "management:user_change_date_format": "/manage/user/<user_id>/change/date-format", "management:change_user_groups": "/manage/user/<user_id>/change/group", "management:user_change_status": "/manage/user/<user_id>/change-status", "management:user_reset_password": "/manage/user/<user_id>/reset-password", "management:user_create": "/manage/users/create", "management:settings": "/manage/settings", "management:change_password": "/manage/settings/change/password", "management:global_settings_general": "/manage/settings/global/general", "management:system_change_app_name": "/manage/settings/system/change/app-name", "management:system_change_app_logo": "/manage/settings/system/change/app-logo", "management:system_remove_app_logo": "/manage/settings/system/remove/app-logo", "management:global_settings_security": "/manage/settings/global/security", "management:system_change_session_expire_time": "/manage/settings/global/security/change/session-expire-time", "management:global_settings_scripts": "/manage/settings/global/scripts", "management:system_active_registration": "/manage/settings/global/active/registration"};
window.reverseUrl = function(urlName) {
  var url = window.routes[urlName];
  if (!url) {
    throw "URL '" + urlName + "' was not found.";
  }

  const args = arguments;
  const argTokens = url.match(/<\w*>/g);
  if (!argTokens && args[1] !== undefined) {
    throw "Invalid URL lookup: URL '" + urlName + "' does not expect any arguments.";
  }

  if (typeof (args[1]) == 'object' && !Array.isArray(args[1])) {
    argTokens.forEach(function(token) {
      const argName = token.slice(1, -1);
      const argValue = args[1][argName];
      if (argValue === undefined) {
        throw "Invalid URL lookup: Argument '" + argName + "' was not provided.";
      }

      url = url.replace(token, argValue);
    });
  } else if (args[1] !== undefined) {
    const argsArray = Array.isArray(args[1]) ? args[1] : Array.prototype.slice.apply(args, [1, args.length]);
    if (argTokens.length !== argsArray.length) {
      throw "Invalid URL lookup: Wrong number of arguments ; expected " + argTokens.length + " arguments.";
    }

    argTokens.forEach(function(token, i) {
      const argValue = argsArray[i];
      url = url.replace(token, argValue);
    });
  }

  return url;
};

