import io
from unittest import mock

import pytest
from django.test.client import MULTIPART_CONTENT
from django.urls import reverse

from apps.accounts.models import EmailAddress
from apps.core import models


@pytest.mark.django_db
def test_index_common_user(auto_login_user):
    """The response should return the Index component"""
    inertia_client, user = auto_login_user()

    url = reverse("core:index")
    response = inertia_client.get(url)
    data = response.json()

    assert response.status_code == 200
    assert data["component"] == "Index"


@pytest.mark.django_db
def test_index_management_user(auto_login_manager_user):
    """The response should return redirect to management index"""
    inertia_client, user = auto_login_manager_user()

    url = reverse("core:index")
    response = inertia_client.get(url)

    assert response.status_code == 302
    assert response.url == "/manage/"


@pytest.mark.django_db
def test_index_settings_common_user(auto_login_user):
    """The response should return redirect to core settings"""
    inertia_client, user = auto_login_user()

    url = reverse("core:index_settings")
    response = inertia_client.get(url)

    assert response.status_code == 302
    assert response.url == "/settings"


@pytest.mark.django_db
def test_index_settings_management_user(auto_login_manager_user):
    """The response should return redirect to management settings"""
    inertia_client, user = auto_login_manager_user()

    url = reverse("core:index_settings")
    response = inertia_client.get(url)

    assert response.status_code == 302
    assert response.url == "/manage/settings"


@pytest.mark.django_db
def test_settings(auto_login_user):
    """The response should return the SettingsIndex component and props"""
    inertia_client, user = auto_login_user()

    url = reverse("core:settings")
    response = inertia_client.get(url)
    data = response.json()

    assert response.status_code == 200
    assert data["component"] == "SettingsIndex"
    assert "unconfirmedEmail" in data["props"]
    assert "userProfile" in data["props"]
    assert "maxSizeFile" in data["props"]
    assert "availableLanguages" in data["props"]
    assert "availableCountries" in data["props"]
    assert "availableDateFormats" in data["props"]
    assert "timeResendEmail" in data["props"]


@pytest.mark.django_db
@mock.patch("apps.accounts.tasks.email_confirmation")
def test_change_email(mock_email_confirm, auto_login_user):
    """The response should return send email confirmation and redirect to core index_settings"""
    mock_email_confirm.return_value = True
    inertia_client, user = auto_login_user()

    url = reverse("core:change_email")
    response_post = inertia_client.post(
        url,
        {"email": "otheremail@test.com", "password": "Qwer.1234"},
        content_type="application/json",
    )

    # Request to other view to see the share props
    url = reverse("core:settings")
    response_index = inertia_client.get(url)
    data = response_index.json()

    assert response_post.status_code == 302
    assert data["props"]["flash"]["success"] == "A confirmation email has been send"


@pytest.mark.django_db
def test_change_email_wrong_password(auto_login_user):
    """The response should return error in password and redirect to core index_settings"""
    inertia_client, user = auto_login_user()

    url = reverse("core:change_email")
    response_post = inertia_client.post(
        url,
        {"email": "otheremail@test.com", "password": "Qwer.123456"},
        content_type="application/json",
    )

    # Request to other view to see the share props
    url = reverse("core:settings")
    response_index = inertia_client.get(url)
    data = response_index.json()

    assert response_post.status_code == 302
    assert data["props"]["flash"]["error"] == "Exists errors on form"
    assert data["props"]["errors"]["password"] == ["Wrong password"]


@pytest.mark.django_db
def test_change_email_email_already_registered(auto_login_user, create_user):
    """The response should return email already registered and redirect to core index_settings"""
    inertia_client, user = auto_login_user()
    # Create CustomUser with other email
    other_user = create_user(email="otheremail@test.com", password="Qwer.1234")

    url = reverse("core:change_email")
    response_post = inertia_client.post(
        url,
        {"email": other_user.email, "password": "Qwer.1234"},
        content_type="application/json",
    )

    # Request to other view to see the share props
    url = reverse("core:settings")
    response_index = inertia_client.get(url)
    data = response_index.json()

    assert response_post.status_code == 302
    assert data["props"]["flash"]["error"] == "Exists errors on form"
    assert data["props"]["errors"]["email"] == ["This email already registered"]


@pytest.mark.django_db
def test_cancel_change_email(auto_login_user):
    """The response should delete email address and return redirect to core index_settings"""
    inertia_client, user = auto_login_user()
    email_address = EmailAddress.get_or_create(user, "otheremail@test.com")

    url = reverse("core:cancel_change_email")
    response_post = inertia_client.post(
        url,
        {"email": email_address.email},
        content_type="application/json",
    )

    # Request to other view to see the share props
    url = reverse("core:settings")
    response_index = inertia_client.get(url)
    data = response_index.json()

    assert response_post.status_code == 302
    assert data["props"]["flash"]["success"] == "Change email canceled"


@pytest.mark.django_db
def test_change_name(auto_login_user):
    """The response should change user names and return redirect to core index_settings"""
    inertia_client, user = auto_login_user()

    url = reverse("core:change_names")
    response_post = inertia_client.post(
        url,
        {"firstName": "jhon", "lastName": "doe"},
        content_type="application/json",
    )

    # Request to other view to see the share props
    url = reverse("core:settings")
    response_index = inertia_client.get(url)
    data = response_index.json()

    assert response_post.status_code == 302
    assert data["props"]["flash"]["success"] == "Successful name change"


@pytest.mark.django_db
def test_change_name_invalid_names(auto_login_user):
    """The response should return invalid names errors and redirect to core index_settings"""
    inertia_client, user = auto_login_user()

    url = reverse("core:change_names")
    response_post = inertia_client.post(
        url,
        {"firstName": "", "lastName": ""},
        content_type="application/json",
    )

    # Request to other view to see the share props
    url = reverse("core:settings")
    response_index = inertia_client.get(url)
    data = response_index.json()

    assert response_post.status_code == 302
    assert data["props"]["flash"]["error"] == "Exists errors on form"


@pytest.mark.django_db
def test_change_job_title(auto_login_user):
    """The response should change user job title and return redirect to core index_settings"""
    inertia_client, user = auto_login_user()
    user_profile = models.UserProfile(user=user)
    user_profile.save()

    url = reverse("core:change_job_title")
    response_post = inertia_client.post(
        url,
        {"jobTitle": "Developer"},
        content_type="application/json",
    )

    # Request to other view to see the share props
    url = reverse("core:settings")
    response_index = inertia_client.get(url)
    data = response_index.json()

    assert response_post.status_code == 302
    assert data["props"]["flash"]["success"] == "Successful job title change"


@pytest.mark.django_db
def test_change_job_title_invalid_form(auto_login_user):
    """The response should return invalid form errors and redirect to core index_settings"""
    inertia_client, user = auto_login_user()
    user_profile = models.UserProfile(user=user)
    user_profile.save()

    url = reverse("core:change_job_title")
    response_post = inertia_client.post(
        url,
        {"jobTitle": ""},
        content_type="application/json",
    )

    # Request to other view to see the share props
    url = reverse("core:settings")
    response_index = inertia_client.get(url)
    data = response_index.json()

    assert response_post.status_code == 302
    assert data["props"]["flash"]["error"] == "Exists errors on form"


@pytest.mark.django_db
def test_change_photo(auto_login_user, test_image_file):
    inertia_client, user = auto_login_user()
    user_profile = models.UserProfile(user=user)
    user_profile.save()

    url = reverse("core:change_photo")
    response_post = inertia_client.post(
        url,
        {"photo": test_image_file},
        content_type=MULTIPART_CONTENT,
    )

    # Request to other view to see the share props
    url = reverse("core:settings")
    response_index = inertia_client.get(url)
    data = response_index.json()

    assert response_post.status_code == 302
    assert data["props"]["flash"]["success"] == "Successful photo change"


@pytest.mark.django_db
def test_change_photo_invalid_type(auto_login_user):
    inertia_client, user = auto_login_user()
    user_profile = models.UserProfile(user=user)
    user_profile.save()

    url = reverse("core:change_photo")
    response_post = inertia_client.post(
        url,
        {"photo": ("photo.jpg", io.BytesIO(b"some random data"), "image/jpg")},
        content_type=MULTIPART_CONTENT,
    )

    # Request to other view to see the share props
    url = reverse("core:settings")
    response_index = inertia_client.get(url)
    data = response_index.json()

    assert response_post.status_code == 302
    assert data["props"]["flash"]["error"] == "Exists errors on form"
    assert data["props"]["errors"]["photo"] == [
        "Invalid file type, please choose another one."
    ]


@pytest.mark.django_db
def test_change_photo_empty_data(auto_login_user):
    inertia_client, user = auto_login_user()
    user_profile = models.UserProfile(user=user)
    user_profile.save()

    url = reverse("core:change_photo")
    response_post = inertia_client.post(
        url,
        {},
        content_type=MULTIPART_CONTENT,
    )

    # Request to other view to see the share props
    url = reverse("core:settings")
    response_index = inertia_client.get(url)
    data = response_index.json()

    assert response_post.status_code == 302
    assert data["props"]["flash"]["error"] == "Exists errors on form"
    assert data["props"]["errors"]["photo"] == ["This field is required."]


@pytest.mark.django_db
def test_remove_photo(auto_login_user):
    inertia_client, user = auto_login_user()
    user_profile = models.UserProfile(user=user)
    user_profile.save()

    url = reverse("core:remove_photo")
    response_post = inertia_client.get(url)

    # Request to other view to see the share props
    url = reverse("core:settings")
    response_index = inertia_client.get(url)
    data = response_index.json()

    assert response_post.status_code == 302
    assert data["props"]["flash"]["success"] == "Photo successfully removed"


@pytest.mark.django_db
def test_change_language(auto_login_user):
    """The response should change user language and return redirect to core index_settings"""
    inertia_client, user = auto_login_user()
    user_profile = models.UserProfile(user=user)
    user_profile.save()

    url = reverse("core:change_language")
    response_post = inertia_client.post(
        url,
        {"language": "es"},
        content_type="application/json",
    )

    # Request to other view to see the share props
    url = reverse("core:settings")
    response_index = inertia_client.get(url)
    data = response_index.json()

    assert response_post.status_code == 302
    assert data["props"]["flash"]["success"] == "Successful language change"


@pytest.mark.django_db
def test_change_language_invalid_form(auto_login_user):
    """The response should return invalid form errors and redirect to core index_settings"""
    inertia_client, user = auto_login_user()
    user_profile = models.UserProfile(user=user)
    user_profile.save()

    url = reverse("core:change_language")
    response_post = inertia_client.post(
        url,
        {"language": ""},
        content_type="application/json",
    )

    # Request to other view to see the share props
    url = reverse("core:settings")
    response_index = inertia_client.get(url)
    data = response_index.json()

    assert response_post.status_code == 302
    assert data["props"]["flash"]["error"] == "Exists errors on form"


@pytest.mark.django_db
def test_change_country(auto_login_user):
    """The response should change user country and return redirect to core index_settings"""
    inertia_client, user = auto_login_user()
    user_profile = models.UserProfile(user=user)
    user_profile.save()

    url = reverse("core:change_country")
    response_post = inertia_client.post(
        url,
        {"country": "es"},
        content_type="application/json",
    )

    # Request to other view to see the share props
    url = reverse("core:settings")
    response_index = inertia_client.get(url)
    data = response_index.json()

    assert response_post.status_code == 302
    assert data["props"]["flash"]["success"] == "Successful country change"


@pytest.mark.django_db
def test_change_country_invalid_form(auto_login_user):
    """The response should return invalid form errors and redirect to core index_settings"""
    inertia_client, user = auto_login_user()
    user_profile = models.UserProfile(user=user)
    user_profile.save()

    url = reverse("core:change_country")
    response_post = inertia_client.post(
        url,
        {"country": ""},
        content_type="application/json",
    )

    # Request to other view to see the share props
    url = reverse("core:settings")
    response_index = inertia_client.get(url)
    data = response_index.json()

    assert response_post.status_code == 302
    assert data["props"]["flash"]["error"] == "Exists errors on form"


@pytest.mark.django_db
def test_change_date_format(auto_login_user):
    """The response should change user date format and return redirect to core index_settings"""
    inertia_client, user = auto_login_user()
    user_profile = models.UserProfile(user=user)
    user_profile.save()

    url = reverse("core:change_date_format")
    response_post = inertia_client.post(
        url,
        {"dateFormat": "MM/DD/YY"},
        content_type="application/json",
    )

    # Request to other view to see the share props
    url = reverse("core:settings")
    response_index = inertia_client.get(url)
    data = response_index.json()

    assert response_post.status_code == 302
    assert data["props"]["flash"]["success"] == "Successful date format change"


@pytest.mark.django_db
def test_change_date_format_invalid_form(auto_login_user):
    """The response should return invalid form errors and redirect to core index_settings"""
    inertia_client, user = auto_login_user()
    user_profile = models.UserProfile(user=user)
    user_profile.save()

    url = reverse("core:change_date_format")
    response_post = inertia_client.post(
        url,
        {"dateFormat": ""},
        content_type="application/json",
    )

    # Request to other view to see the share props
    url = reverse("core:settings")
    response_index = inertia_client.get(url)
    data = response_index.json()

    assert response_post.status_code == 302
    assert data["props"]["flash"]["error"] == "Exists errors on form"


@pytest.mark.django_db
def test_error_400(inertia_client):
    """The response should return the 400Error component"""

    url = reverse("core:error_400")
    response = inertia_client.get(url)
    data = response.json()

    assert response.status_code == 200
    assert data["component"] == "400Error"


@pytest.mark.django_db
def test_error_403(inertia_client):
    """The response should return the 403Error component"""

    url = reverse("core:error_403")
    response = inertia_client.get(url)
    data = response.json()

    assert response.status_code == 200
    assert data["component"] == "403Error"


@pytest.mark.django_db
def test_error_404(inertia_client):
    """The response should return the 404Error component"""

    url = reverse("core:error_404")
    response = inertia_client.get(url)
    data = response.json()

    assert response.status_code == 200
    assert data["component"] == "404Error"


@pytest.mark.django_db
def test_error_500(inertia_client):
    """The response should return the 500Error component"""

    url = reverse("core:error_500")
    response = inertia_client.get(url)
    data = response.json()

    assert response.status_code == 200
    assert data["component"] == "500Error"
