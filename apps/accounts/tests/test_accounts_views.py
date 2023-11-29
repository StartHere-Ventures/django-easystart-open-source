from unittest import mock

import pytest
from django.contrib.auth.tokens import default_token_generator
from django.urls import reverse
from django.utils import timezone

from apps.accounts.models import EmailAddress, EmailConfirmation
from apps.accounts.utils import user_pk_to_url_str


@pytest.mark.django_db
def test_login_view_get(inertia_client):
    """The response should return the Login component and props"""
    url = reverse("accounts:login")
    response = inertia_client.get(url)
    data = response.json()

    assert response.status_code == 200
    assert data["component"] == "Login"


@pytest.mark.django_db
def test_login_view_authenticate_user(inertia_client, create_user, test_password):
    """The response should return a redirect to ACCOUNT_LOGIN_REDIRECT_URL"""
    user = create_user()
    password = test_password
    url = reverse("accounts:login")
    response = inertia_client.post(
        url,
        {"email": user.email, "password": password},
        content_type="application/json",
    )

    # Redirect Response to ACCOUNT_LOGIN_REDIRECT_URL
    assert response.status_code == 302


@pytest.mark.django_db
def test_login_view_wrong_credentials_authenticate_user(inertia_client, create_user):
    """The response should return an error with invalid credentials"""
    user = create_user()
    url = reverse("accounts:login")
    response = inertia_client.post(
        url,
        {"email": user.email, "password": "password"},
        content_type="application/json",
    )
    data = response.json()

    assert response.status_code == 200
    assert data["props"]["error"] == "Invalid email or password"


@pytest.mark.django_db
def test_login_view_empty_email_or_password_authenticate_user(
    inertia_client, create_user
):
    """The response should return an error when email or password are empty"""
    user = create_user()
    url = reverse("accounts:login")
    response = inertia_client.post(
        url,
        {"email": user.email},
        content_type="application/json",
    )
    data = response.json()

    assert response.status_code == 200
    assert data["props"]["error"] == "Exists errors on form"


@pytest.mark.django_db
def test_logout_view(auto_login_user):
    """The response should return a redirect to ACCOUNT_LOGOUT_REDIRECT_URL"""
    inertia_client, user = auto_login_user()
    url = reverse("accounts:logout")
    response = inertia_client.get(url)

    # Redirect Response to ACCOUNT_LOGOUT_REDIRECT_URL
    assert response.status_code == 302


@pytest.mark.django_db
def test_register_view_get(inertia_client):
    """The response should return the Register component and props"""
    url = reverse("accounts:register")
    response = inertia_client.get(url)
    data = response.json()

    assert response.status_code == 200
    assert data["component"] == "Register"
    assert "paramsPasswordValidator" in data["props"]


@pytest.mark.django_db
def test_register_view_signup_user(inertia_client):
    """The response should return a redirect to ACCOUNT_LOGIN_REDIRECT_URL"""
    url = reverse("accounts:register")
    response = inertia_client.post(
        url,
        {
            "email": "jhondoe@test.com",
            "password": "Qwer.1234",
            "firstName": "Jhon",
            "lastName": "Doe",
        },
        content_type="application/json",
    )

    # Redirect Response to ACCOUNT_LOGIN_REDIRECT_URL
    assert response.status_code == 302


@pytest.mark.django_db
def test_register_view_empty_email_or_password_signup_user(inertia_client):
    """The response should return an error when email or password are empty"""
    url = reverse("accounts:register")
    response = inertia_client.post(
        url,
        {
            "firstName": "Jhon",
            "lastName": "Doe",
        },
        content_type="application/json",
    )
    data = response.json()

    assert response.status_code == 200
    assert data["props"]["error"] == "Exists errors on form"


@pytest.mark.django_db
def test_email_verification_sent_get(inertia_client):
    """The response should return the EmailVerificationSend component"""
    url = reverse("accounts:email_verification_sent")
    response = inertia_client.get(url)
    data = response.json()

    assert response.status_code == 200
    assert data["component"] == "EmailVerificationSend"


@pytest.mark.django_db
@mock.patch("apps.accounts.tasks.email_confirmation")
def test_email_verification_sent_email_is_sending(
    mock_email_confirm, inertia_client, create_user
):
    """The response should return a redirect to login view"""
    mock_email_confirm.return_value = True
    user = create_user()
    url = reverse("accounts:email_verification_sent")
    response = inertia_client.post(
        url,
        {
            "email": user.email,
        },
        content_type="application/json",
    )

    # Redirect Response to login
    assert response.status_code == 302


@pytest.mark.django_db
def test_email_verification_sent_email_is_empty(inertia_client):
    """The response should return an error when email is empty"""
    url = reverse("accounts:email_verification_sent")
    response = inertia_client.post(
        url,
        {},
        content_type="application/json",
    )
    data = response.json()

    assert response.status_code == 200
    assert data["props"]["error"] == "Exists errors on form"


@pytest.mark.django_db
def test_email_verification_sent_with_email_not_registered(inertia_client):
    """The response should return an error when email is not registered"""
    url = reverse("accounts:email_verification_sent")
    response = inertia_client.post(
        url,
        {"email": "otheruser@test.com"},
        content_type="application/json",
    )
    data = response.json()

    assert response.status_code == 200
    assert data["props"]["error"] == "This email is not registered"


@pytest.mark.django_db
def test_confirm_email_invalid_key(inertia_client):
    """The response should return the ConfirmEmail component"""
    url = reverse("accounts:confirm_email", args=("123456",))
    response = inertia_client.get(url)
    data = response.json()

    assert response.status_code == 200
    assert data["component"] == "ConfirmEmail"


@pytest.mark.django_db
def test_confirm_email_valid_key(inertia_client, create_user):
    """The response should return a redirect to LOGIN_ON_EMAIL_CONFIRMATION"""
    user = create_user()
    email_address = EmailAddress.get_or_create(user, user.email)
    confirmation = EmailConfirmation.create(email_address)
    confirmation.sent = timezone.now()
    confirmation.save()

    url = reverse("accounts:confirm_email", args=(confirmation.key,))
    response = inertia_client.get(url)

    # Redirect Response to LOGIN_ON_EMAIL_CONFIRMATION
    assert response.status_code == 302


@pytest.mark.django_db
def test_password_reset_get(inertia_client):
    """The response should return the PasswordReset component"""
    url = reverse("accounts:reset_password")
    response = inertia_client.get(url)
    data = response.json()

    assert response.status_code == 200
    assert data["component"] == "PasswordReset"


@pytest.mark.django_db
@mock.patch("apps.accounts.tasks.email_password_reset")
def test_password_reset_email_is_sending(
    mock_email_confirm, inertia_client, create_user
):
    """The response should return a redirect to login view"""
    mock_email_confirm.return_value = True
    user = create_user()
    url = reverse("accounts:reset_password")
    response = inertia_client.post(
        url,
        {
            "email": user.email,
        },
        content_type="application/json",
    )

    # Redirect Response to login
    assert response.status_code == 302


@pytest.mark.django_db
def test_password_reset_email_is_empty(inertia_client):
    """The response should return an error when email is empty"""
    url = reverse("accounts:reset_password")
    response = inertia_client.post(
        url,
        {},
        content_type="application/json",
    )
    data = response.json()

    assert response.status_code == 200
    assert data["props"]["error"] == "Exists errors on form"


@pytest.mark.django_db
def test_password_reset_with_email_not_registered(inertia_client):
    """The response should return an error when email is not registered"""
    url = reverse("accounts:reset_password")
    response = inertia_client.post(
        url,
        {"email": "otheruser@test.com"},
        content_type="application/json",
    )
    data = response.json()

    assert response.status_code == 200
    assert data["props"]["error"] == "This email is not registered"


@pytest.mark.django_db
def test_password_reset_from_key(inertia_client):
    """The response should return the SetPasswordFromKey component and props"""
    url = reverse("accounts:reset_password_from_key", args=("123", "123456"))
    response = inertia_client.get(url)
    data = response.json()

    assert response.status_code == 200
    assert data["component"] == "SetPasswordFromKey"
    assert "uidb36" in data["props"]
    assert "keyToken" in data["props"]
    assert "tokenInvalid" in data["props"]
    assert "paramsPasswordValidator" in data["props"]


@pytest.mark.django_db
def test_password_reset_from_key_with_authenticated_user(auto_login_user):
    """The response should return the SetPasswordFromKey component and props"""
    inertia_client, user = auto_login_user()
    url = reverse("accounts:reset_password_from_key", args=("random", "random"))
    response = inertia_client.get(url)
    data = response.json()

    assert response.status_code == 200
    assert data["component"] == "SetPasswordFromKey"
    assert "uidb36" in data["props"]
    assert "keyToken" in data["props"]
    assert "tokenInvalid" in data["props"]
    assert "paramsPasswordValidator" in data["props"]


@pytest.mark.django_db
def test_password_reset_from_key_with_valid_key_and_valid_password(
    inertia_client, create_user
):
    """The response should return change password and redirect to login view"""
    user = create_user()
    token_generator = default_token_generator
    temp_key = token_generator.make_token(user)
    uidb36 = user_pk_to_url_str(user)

    url = reverse("accounts:reset_password_from_key", args=(uidb36, temp_key))
    response = inertia_client.post(
        url,
        {"password": "Qwer.1234"},
        content_type="application/json",
    )

    # Redirect Response to login
    assert response.status_code == 302


@pytest.mark.django_db
def test_password_reset_from_key_with_valid_key_and_empty_password(
    inertia_client, create_user
):
    """The response should return an error when password is empty"""
    user = create_user()
    token_generator = default_token_generator
    temp_key = token_generator.make_token(user)
    uidb36 = user_pk_to_url_str(user)

    url = reverse("accounts:reset_password_from_key", args=(uidb36, temp_key))
    response = inertia_client.post(
        url,
        {},
        content_type="application/json",
    )
    data = response.json()

    assert response.status_code == 200
    assert data["props"]["error"] == "Exists errors on form"


@pytest.mark.django_db
def test_password_reset_from_key_with_invalid_key(inertia_client, create_user):
    """The response should return an error when key is invalid"""
    user = create_user()
    uidb36 = user_pk_to_url_str(user)

    url = reverse("accounts:reset_password_from_key", args=(uidb36, "123456"))
    response = inertia_client.post(
        url,
        {"password": "Qwer.1234"},
        content_type="application/json",
    )
    data = response.json()

    assert response.status_code == 200
    assert data["props"]["tokenInvalid"]


@pytest.mark.django_db
def test_change_password(auto_login_user):
    """The response should return the ChangePassword"""
    inertia_client, user = auto_login_user()
    url = reverse("accounts:change_password")
    response = inertia_client.get(url)
    data = response.json()

    assert response.status_code == 200
    assert data["component"] == "ChangePassword"


@pytest.mark.django_db
@mock.patch("apps.accounts.tasks.email_password_reset")
def test_change_password_send_email_with_instructions(
    mock_email_password_reset, auto_login_user
):
    """The response should return the ChangePassword and send email with instructions"""
    mock_email_password_reset.return_value = True
    inertia_client, user = auto_login_user()
    url = reverse("accounts:change_password")
    response = inertia_client.post(url)
    data = response.json()

    assert response.status_code == 200
    assert data["component"] == "ChangePassword"
    assert (
        data["props"]["success"]
        == "An email has been sent with instructions to reset your password"
    )


@pytest.mark.django_db
def test_resend_email_verification_api_not_user_authenticated(inertia_client):
    """The response should return an error because user need be authenticated"""
    url = reverse("accounts:resend_email_verification")
    response = inertia_client.get(url)
    data = response.json()

    assert response.status_code == 400
    assert data["status"] == "false"
    assert data["message"] == "Login required"


@pytest.mark.django_db
@mock.patch("apps.accounts.tasks.email_confirmation")
def test_resend_email_verification_api_user_authenticated(
    mock_email_confirm, auto_login_user
):
    """The response should send email to confirm email user account"""
    mock_email_confirm.return_value = True
    inertia_client, user = auto_login_user()
    url = reverse("accounts:resend_email_verification")
    response = inertia_client.get(url)
    data = response.json()

    assert response.status_code == 200
    assert data["success"]
    assert "timeResendEmail" in data
