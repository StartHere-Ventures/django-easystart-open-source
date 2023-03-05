from django.conf import settings
from django_countries import countries


def get_dict_language():
    language = {lang[0]: lang[1] for lang in settings.LANGUAGES}
    return language


def get_array_language():
    language = [lang[0] for lang in settings.LANGUAGES]
    return language


def get_dict_countries():
    dict_countries = {country.code: country.name for country in countries}
    return dict_countries
