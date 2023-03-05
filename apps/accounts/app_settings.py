import sys

from django.conf import settings


class AppSettings(object):
    class EmailVerificationMethod:
        # After signing up, keep the user account inactive until the email
        # address is verified
        MANDATORY = "mandatory"
        # Allow login with unverified e-mail (e-mail verification is
        # still sent)
        OPTIONAL = "optional"
        # Don't send e-mail verification mails during signup
        NONE = "none"

    def _setting(self, name, default):
        return getattr(settings, name, default)

    @property
    def DEFAULT_HTTP_PROTOCOL(self):
        return self._setting("DEFAULT_HTTP_PROTOCOL", "http").lower()

    @property
    def ACCOUNT_LOGIN_ON_SIGNIN(self):
        """
        Automatically log the user in once they sigin
        """
        return self._setting("ACCOUNT_LOGIN_ON_SIGNIN", True)

    @property
    def ACCOUNT_SIGNIN_REDIRECT_URL(self):
        """
        Redirect user in once they signin and ACCOUNT_LOGIN_ON_SIGNIN if False
        """
        return self._setting("ACCOUNT_SIGNIN_REDIRECT_URL", "/login")

    @property
    def ACCOUNT_LOGIN_REDIRECT_URL(self):
        return self._setting("ACCOUNT_LOGIN_REDIRECT_URL", "/")

    @property
    def ACCOUNT_LOGOUT_REDIRECT_URL(self):
        return self._setting("ACCOUNT_LOGOUT_REDIRECT_URL", "/")

    @property
    def EMAIL_VERIFICATION(self):
        """
        See e-mail verification method
        """
        ret = self._setting("EMAIL_VERIFICATION", self.EmailVerificationMethod.OPTIONAL)
        # Deal with legacy (boolean based) setting
        if ret is True:
            ret = self.EmailVerificationMethod.MANDATORY
        elif ret is False:
            ret = self.EmailVerificationMethod.OPTIONAL
        return ret

    @property
    def UNIQUE_EMAIL(self):
        """
        Enforce uniqueness of e-mail addresses
        """
        return self._setting("UNIQUE_EMAIL", True)

    @property
    def MAX_EMAIL_ADDRESSES(self):
        return self._setting("MAX_EMAIL_ADDRESSES", None)

    @property
    def EMAIL_CONFIRMATION_EXPIRE_DAYS(self):
        """
        Determines the expiration date of e-mail confirmation mails (#
        of days)
        """
        return self._setting("EMAIL_CONFIRMATION_EXPIRE_DAYS", 3)

    @property
    def EMAIL_CONFIRMATION_AUTHENTICATED_REDIRECT_URL(self):
        """
        The URL to redirect to after a successful e-mail confirmation, in
        case of an authenticated user
        """
        return self._setting("EMAIL_CONFIRMATION_AUTHENTICATED_REDIRECT_URL", "/login")

    @property
    def EMAIL_CONFIRMATION_COOLDOWN(self):
        """
        The cooldown in seconds during which, after an email confirmation has
        been sent, a second confirmation email will not be sent.
        """
        return self._setting("EMAIL_CONFIRMATION_COOLDOWN", 3 * 60)

    @property
    def EMAIL_FROM_ADDR(self):
        return self._setting("EMAIL_FROM_ADDR", "admin@easystart.com")

    @property
    def LOGIN_ON_EMAIL_CONFIRMATION(self):
        """
        Automatically log the user in once they confirmed their email address
        """
        return self._setting("LOGIN_ON_EMAIL_CONFIRMATION", False)

    @property
    def SOCIAL_ACCOUNT_PROVIDERS(self):
        """
        Social Account Provider specific settings
        """
        return self._setting(
            "SOCIAL_ACCOUNT_PROVIDERS",
            {
                "google": {
                    "SCOPE": ["email", "profile"],
                    "AUTH_PARAMS": {
                        "access_type": "online",
                        "response_type": "code",
                        "prompt": "select_account",
                    },
                    "AUTHURL": "https://accounts.google.com/o/oauth2/v2/auth",
                    "ACCESS_TOKEN_URL": "https://accounts.google.com/o/oauth2/token",
                    "USER_INFO_URL": "https://www.googleapis.com/oauth2/v1/userinfo",
                },
            },
        )


app_settings = AppSettings()
app_settings.__name__ = __name__
sys.modules[__name__] = app_settings
