import sys

from django.conf import settings


class AppSettings(object):
    def _setting(self, name, default):
        return getattr(settings, name, default)

    @property
    def EMAIL_SUBJECT_PREFIX(self):
        """
        Subject-line prefix to use for email messages sent
        """
        return self._setting("EMAIL_SUBJECT_PREFIX", None)

    @property
    def MAX_SIZE_FILE(self):
        return self._setting("MAX_SIZE_FILE", 10)

    @property
    def SESSION_EXPIRE_TIME(self):
        """Duration of session inactivity expresed in min"""
        return self._setting("SESSION_EXPIRE_TIME", 60)


app_settings = AppSettings()
app_settings.__name__ = __name__
sys.modules[__name__] = app_settings
