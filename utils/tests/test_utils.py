import json
from unittest.mock import Mock

import pytest
from django.test import RequestFactory

from utils import build_dict_language, decorator


def test_build_dict_language_get_dict_language():
    """Get an object with all language of the system"""
    languages = build_dict_language.get_dict_language()

    assert isinstance(languages, type({}))
    assert "es" in languages
    assert "en-us" in languages


def test_build_dict_language_get_array_language():
    """Get an object with all language of the system"""
    languages = build_dict_language.get_array_language()

    assert isinstance(languages, type([]))
    assert "es" in languages
    assert "en-us" in languages


def test_build_dict_language_get_dict_countries():
    """Get an object with all language of the system"""
    countries = build_dict_language.get_dict_countries()

    assert isinstance(countries, type({}))
    assert "ES" in countries
    assert "US" in countries


@pytest.mark.django_db
def test_json_format_required_decorator_wrong_format_mock():
    """Return error for bad json format in data"""

    func = Mock()
    decorated_func = decorator.json_format_required(func)

    request = RequestFactory().post("/a/url")
    request.data = "TEXT"
    request.method = "POST"

    response = decorated_func(request)
    data = json.loads(response.content)

    assert response.status_code == 400
    assert data["error"]
    assert data["message"] == "Json format required in data"
