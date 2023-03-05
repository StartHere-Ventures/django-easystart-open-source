import io
from itertools import product
from typing import Optional, Union
from unittest import mock

import pytest
from django.contrib.auth.models import Group
from django.test.client import MULTIPART_CONTENT
from django.urls import reverse

from apps.core import models as core_models


class TestIndex:
    """Tests for the `index` view."""

    @pytest.mark.django_db
    def test_manager(self, auto_login_manager_user):
        """The response should return the Index component."""
        inertia_client, user = auto_login_manager_user()

        url = reverse("management:index")

        response = inertia_client.get(url)
        assert response.status_code == 200

        data = response.json()
        assert data["component"] == "Index"

    @pytest.mark.django_db
    def test_not_authenticated(self, inertia_client):
        """The response should redirect to the login URL."""
        url = reverse("management:index")

        response = inertia_client.get(url)
        assert response.status_code == 302
        assert response.url == "/login"


class TestUsersList:
    """Tests for the `users_list` view."""

    @pytest.mark.django_db
    def test_manager(self, auto_login_manager_user):
        """The response should return the Users component and props."""
        inertia_client, user = auto_login_manager_user()
        assert user.has_perm("core.can_view_users")

        url = reverse("management:users")
        response = inertia_client.get(url)
        assert response.status_code == 200

        data = response.json()
        assert data["component"] == "Users"
        assert "count" in data["props"]
        assert "paginateBy" in data["props"]
        assert "pages" in data["props"]
        assert "currentPage" in data["props"]
        assert "users" in data["props"]

    @pytest.mark.django_db
    def test_client(self, auto_login_user):
        """Client user should not have permission to access the view."""
        inertia_client, user = auto_login_user()
        assert not user.has_perm("core.can_view_users")

        url = reverse("management:users")
        response = inertia_client.get(url)
        assert response.status_code == 200

        data = response.json()
        assert data["component"] == "403Error"

    @pytest.mark.django_db
    @pytest.mark.parametrize("grant_permission", [False, True])
    def test_custom(
        self,
        auto_login_custom_user,
        grant_permissions_custom_group,
        grant_permission: bool,
    ):
        """
        Custom users should only be able to access the view if their group
        has the required permission.
        """
        inertia_client, user = auto_login_custom_user()

        if grant_permission:
            grant_permissions_custom_group("can_view_users")
            assert user.has_perm("core.can_view_users")
        else:
            assert not user.has_perm("core.can_view_users")

        url = reverse("management:users")
        response = inertia_client.get(url)
        assert response.status_code == 200

        data = response.json()
        if grant_permission:
            assert data["component"] == "Users"
            assert "count" in data["props"]
            assert "paginateBy" in data["props"]
            assert "pages" in data["props"]
            assert "currentPage" in data["props"]
            assert "users" in data["props"]
        else:
            assert data["component"] == "403Error"

    @pytest.mark.django_db
    def test_not_authenticated(self, inertia_client):
        """The response should redirect to the login URL."""
        url = reverse("management:users")

        response = inertia_client.get(url)
        assert response.status_code == 302
        assert response.url == "/login"


class TestUserDetail:
    """Tests for the `user_detail` view."""

    @pytest.mark.django_db
    def test_manager(self, auto_login_manager_user, create_user):
        """The response should return the UserDetail component and props."""
        inertia_client, user = auto_login_manager_user()
        assert user.has_perm("core.can_view_user_detail")

        common_user = create_user(
            email="commonuser@test.com", first_name="Common", last_name="User"
        )

        url = reverse("management:user_detail", args=(common_user.id,))
        response = inertia_client.get(url)
        assert response.status_code == 200

        data = response.json()
        assert data["component"] == "UserDetail"
        assert "user" in data["props"]
        assert "maxSizeFile" in data["props"]
        assert "availableLanguages" in data["props"]
        assert "availableCountries" in data["props"]
        assert "availableGroups" in data["props"]
        assert "availableDateFormats" in data["props"]

    @pytest.mark.django_db
    def test_manager_invalid_id(self, auto_login_manager_user):
        """The response should return error and redirect to user_list."""
        inertia_client, user = auto_login_manager_user()
        assert user.has_perm("core.can_view_user_detail")

        url = reverse("management:user_detail", args=("3534465",))
        response = inertia_client.get(url)
        assert response.status_code == 302
        assert response.url == reverse("management:users")

        # Request to other view to see the share props
        response = inertia_client.get(response.url)
        assert response.status_code == 200

        data = response.json()
        assert data["props"]["errors"] == "This user does not exist"

    @pytest.mark.django_db
    def test_client(self, auto_login_user, create_user):
        """Client user should not have permission to access the view."""
        inertia_client, user = auto_login_user()
        assert not user.has_perm("core.can_view_user_detail")

        common_user = create_user(
            email="commonuser@test.com", first_name="Common", last_name="User"
        )

        url = reverse("management:user_detail", args=(common_user.id,))
        response = inertia_client.get(url)
        assert response.status_code == 200

        data = response.json()
        assert data["component"] == "403Error"

    @pytest.mark.django_db
    @pytest.mark.parametrize("grant_permission", [False, True])
    def test_custom(
        self,
        auto_login_custom_user,
        create_user,
        grant_permissions_custom_group,
        grant_permission: bool,
    ):
        """
        Custom users should only be able to access the view if their group
        has the required permission.
        """
        inertia_client, user = auto_login_custom_user()

        if grant_permission:
            grant_permissions_custom_group("can_view_user_detail")
            assert user.has_perm("core.can_view_user_detail")
        else:
            assert not user.has_perm("core.can_view_user_detail")

        common_user = create_user(
            email="commonuser@test.com", first_name="Common", last_name="User"
        )

        url = reverse("management:user_detail", args=(common_user.id,))
        response = inertia_client.get(url)
        assert response.status_code == 200

        data = response.json()
        if grant_permission:
            assert data["component"] == "UserDetail"
            assert "user" in data["props"]
            assert "maxSizeFile" in data["props"]
            assert "availableLanguages" in data["props"]
            assert "availableCountries" in data["props"]
            assert "availableGroups" in data["props"]
            assert "availableDateFormats" in data["props"]
        else:
            assert data["component"] == "403Error"

    @pytest.mark.django_db
    def test_not_authenticated(self, inertia_client, create_user):
        """The response should redirect to the login URL."""
        common_user = create_user(
            email="commonuser@test.com", first_name="Common", last_name="User"
        )

        url = reverse("management:user_detail", args=(common_user.id,))

        response = inertia_client.get(url)
        assert response.status_code == 302
        assert response.url == "/login"


class TestUserChangeStatus:
    """Tests for the `user_change_status` view."""

    @pytest.mark.django_db
    @pytest.mark.parametrize("initial_is_active", [None, False, True])
    def test_manager(
        self, auto_login_manager_user, create_user, initial_is_active: Optional[bool]
    ):
        """The response should change user status and return redirect to user_detail."""
        inertia_client, user = auto_login_manager_user()
        assert user.has_perm("core.can_edit_user")

        common_user = create_user(
            email="commonuser@test.com", first_name="Common", last_name="User"
        )

        if initial_is_active is None:
            initial_is_active = common_user.is_active
        else:
            common_user.is_active = initial_is_active
            common_user.save()

        url = reverse("management:user_change_status", args=(common_user.id,))
        response = inertia_client.get(url)
        assert response.status_code == 302
        assert response.url == reverse("management:user_detail", args=(common_user.id,))

        # Request to other view to see the share props
        response = inertia_client.get(response.url)
        assert response.status_code == 200

        data = response.json()
        assert data["props"]["flash"]["success"] == "Successful status change"

        # Verify change of status
        common_user = core_models.CustomUser.objects.get(id=common_user.id)
        if initial_is_active:
            assert not common_user.is_active
        else:
            assert common_user.is_active

    @pytest.mark.django_db
    def test_manager_invalid_id(self, auto_login_manager_user):
        """The response should return error and redirect to user_list."""
        inertia_client, user = auto_login_manager_user()
        assert user.has_perm("core.can_edit_user")

        url = reverse("management:user_change_status", args=("3534465",))
        response = inertia_client.get(url)
        assert response.status_code == 302
        assert response.url == reverse("management:users")

        # Request to other view to see the share props
        response = inertia_client.get(response.url)
        assert response.status_code == 200

        data = response.json()
        assert data["props"]["errors"] == "This user does not exist"

    @pytest.mark.django_db
    def test_client(self, auto_login_user, create_user):
        """Client user should not have permission to access the view."""
        inertia_client, user = auto_login_user()
        assert not user.has_perm("core.can_edit_user")

        common_user = create_user(
            email="commonuser@test.com", first_name="Common", last_name="User"
        )

        url = reverse("management:user_change_status", args=(common_user.id,))
        response = inertia_client.get(url)
        assert response.status_code == 200

        data = response.json()
        assert data["component"] == "403Error"

    @pytest.mark.django_db
    @pytest.mark.parametrize("grant_permission", [False, True])
    def test_custom(
        self,
        auto_login_custom_user,
        create_user,
        grant_permissions_custom_group,
        grant_permission: bool,
    ):
        """
        Custom users should only be able to access the view if their group
        has the required permission.
        """
        inertia_client, user = auto_login_custom_user()

        if grant_permission:
            grant_permissions_custom_group("can_edit_user")
            assert user.has_perm("core.can_edit_user")
        else:
            assert not user.has_perm("core.can_edit_user")

        common_user = create_user(
            email="commonuser@test.com", first_name="Common", last_name="User"
        )

        initial_is_active = common_user.is_active

        url = reverse("management:user_change_status", args=(common_user.id,))
        response = inertia_client.get(url)

        if grant_permission:
            assert response.status_code == 302
            assert response.url == reverse(
                "management:user_detail", args=(common_user.id,)
            )

            # Request to other view to see the share props
            response = inertia_client.get(response.url)
            assert response.status_code == 200

            data = response.json()
            assert data["props"]["flash"]["success"] == "Successful status change"

            # Verify change of status
            common_user = core_models.CustomUser.objects.get(id=common_user.id)
            if initial_is_active:
                assert not common_user.is_active
            else:
                assert common_user.is_active
        else:
            assert response.status_code == 200

            data = response.json()
            assert data["component"] == "403Error"

    @pytest.mark.django_db
    def test_not_authenticated(self, inertia_client, create_user):
        """The response should redirect to the login URL."""
        common_user = create_user(
            email="commonuser@test.com", first_name="Common", last_name="User"
        )

        url = reverse("management:user_change_status", args=(common_user.id,))

        response = inertia_client.get(url)
        assert response.status_code == 302
        assert response.url == "/login"


class TestUserResetPassword:
    """Tests for the `user_reset_password` view."""

    @pytest.mark.django_db
    @mock.patch("apps.accounts.tasks.email_password_reset")
    def test_manager(
        self, mock_email_password_reset, auto_login_manager_user, create_user
    ):
        """
        The response should send email to reset password and return redirect to
        user_detail.
        """
        mock_email_password_reset.return_value = True
        inertia_client, user = auto_login_manager_user()
        assert user.has_perm("core.can_edit_user")

        common_user = create_user(
            email="commonuser@test.com", first_name="Common", last_name="User"
        )

        url = reverse("management:user_reset_password", args=(common_user.id,))
        response = inertia_client.get(url)
        assert response.status_code == 302
        assert response.url == reverse("management:user_detail", args=(common_user.id,))

        # Request to other view to see the share props
        response = inertia_client.get(response.url)
        assert response.status_code == 200

        data = response.json()
        assert data["props"]["flash"]["success"] == "Email sent"

    @pytest.mark.django_db
    def test_manager_invalid_id(self, auto_login_manager_user):
        """The response should return error and redirect to user_list."""
        inertia_client, user = auto_login_manager_user()
        assert user.has_perm("core.can_edit_user")

        url = reverse("management:user_reset_password", args=("2423432",))
        response = inertia_client.get(url)
        assert response.status_code == 302
        assert response.url == reverse("management:users")

        # Request to other view to see the share props
        response = inertia_client.get(response.url)
        assert response.status_code == 200

        data = response.json()
        assert data["props"]["errors"] == "This user does not exist"

    @pytest.mark.django_db
    def test_client(self, auto_login_user, create_user):
        """Client user should not have permission to access the view."""
        inertia_client, user = auto_login_user()
        assert not user.has_perm("core.can_edit_user")

        common_user = create_user(
            email="commonuser@test.com", first_name="Common", last_name="User"
        )

        url = reverse("management:user_reset_password", args=(common_user.id,))
        response = inertia_client.get(url)
        assert response.status_code == 200

        data = response.json()
        assert data["component"] == "403Error"

    @pytest.mark.django_db
    @pytest.mark.parametrize("grant_permission", [False, True])
    @mock.patch("apps.accounts.tasks.email_password_reset")
    def test_custom(
        self,
        mock_email_password_reset,
        auto_login_custom_user,
        create_user,
        grant_permissions_custom_group,
        grant_permission: bool,
    ):
        """
        Custom users should only be able to access the view if their group
        has the required permission.
        """
        mock_email_password_reset.return_value = True
        inertia_client, user = auto_login_custom_user()

        if grant_permission:
            grant_permissions_custom_group("can_edit_user")
            assert user.has_perm("core.can_edit_user")
        else:
            assert not user.has_perm("core.can_edit_user")

        common_user = create_user(
            email="commonuser@test.com", first_name="Common", last_name="User"
        )

        url = reverse("management:user_reset_password", args=(common_user.id,))
        response = inertia_client.get(url)

        if grant_permission:
            assert response.status_code == 302
            assert response.url == reverse(
                "management:user_detail", args=(common_user.id,)
            )

            # Request to other view to see the share props
            response = inertia_client.get(response.url)
            assert response.status_code == 200

            data = response.json()
            assert data["props"]["flash"]["success"] == "Email sent"
        else:
            assert response.status_code == 200

            data = response.json()
            assert data["component"] == "403Error"

    @pytest.mark.django_db
    def test_not_authenticated(self, inertia_client, create_user):
        """The response should redirect to the login URL."""
        common_user = create_user(
            email="commonuser@test.com", first_name="Common", last_name="User"
        )

        url = reverse("management:user_reset_password", args=(common_user.id,))

        response = inertia_client.get(url)
        assert response.status_code == 302
        assert response.url == "/login"


class TestUserChangeNames:
    """Tests for the `user_change_names` view."""

    @pytest.mark.django_db
    @pytest.mark.parametrize(
        ["first_name", "last_name"], list(product(["", "John"], ["", "Doe"]))
    )
    def test_manager(
        self, auto_login_manager_user, create_user, first_name: str, last_name: str
    ):
        """
        The response should change the user's names and return redirect to
        user_detail.
        """
        inertia_client, user = auto_login_manager_user()
        assert user.has_perm("core.can_edit_user")

        common_user = create_user(
            email="commonuser@test.com", first_name="Common", last_name="User"
        )

        url = reverse("management:user_change_names", args=(common_user.id,))
        post_data = {"firstName": first_name, "lastName": last_name}
        response = inertia_client.post(
            url, data=post_data, content_type="application/json"
        )
        assert response.status_code == 302
        assert response.url == reverse("management:user_detail", args=(common_user.id,))

        # Request to other view to see the share props
        response = inertia_client.get(response.url)
        assert response.status_code == 200

        data = response.json()

        common_user = core_models.CustomUser.objects.get(id=common_user.id)

        if first_name and last_name:
            assert data["props"]["flash"]["success"] == "Successful name change"

            # Verify names changed
            assert common_user.first_name == first_name
            assert common_user.last_name == last_name
        else:
            assert data["props"]["flash"]["error"] == "Exists errors on form"

            # Verify names did not change
            assert common_user.first_name == "Common"
            assert common_user.last_name == "User"

    @pytest.mark.django_db
    def test_manager_invalid_id(self, auto_login_manager_user):
        """The response should return error and redirect to user_list."""
        inertia_client, user = auto_login_manager_user()
        assert user.has_perm("core.can_edit_user")

        url = reverse("management:user_change_names", args=("3534465",))
        post_data = {"firstName": "John", "lastName": "Doe"}
        response = inertia_client.post(
            url, data=post_data, content_type="application/json"
        )
        assert response.status_code == 302
        assert response.url == reverse("management:users")

        # Request to other view to see the share props
        response = inertia_client.get(response.url)
        assert response.status_code == 200

        data = response.json()
        assert data["props"]["errors"] == "This user does not exist"

    @pytest.mark.django_db
    def test_client(self, auto_login_user, create_user):
        """Client user should not have permission to access the view."""
        inertia_client, user = auto_login_user()
        assert not user.has_perm("core.can_edit_user")

        common_user = create_user(
            email="commonuser@test.com", first_name="Common", last_name="User"
        )

        url = reverse("management:user_change_names", args=(common_user.id,))
        post_data = {"firstName": "John", "lastName": "Doe"}
        response = inertia_client.post(
            url, data=post_data, content_type="application/json"
        )
        # Inertia client somehow tries to request a GET view (probably 403_error)
        assert response.status_code == 405

        # Verify names did not change
        common_user = core_models.CustomUser.objects.get(id=common_user.id)
        assert common_user.first_name == "Common"
        assert common_user.last_name == "User"

    @pytest.mark.django_db
    @pytest.mark.parametrize("grant_permission", [False, True])
    def test_custom(
        self,
        auto_login_custom_user,
        create_user,
        grant_permissions_custom_group,
        grant_permission: bool,
    ):
        """
        Custom users should only be able to access the view if their group
        has the required permission.
        """
        inertia_client, user = auto_login_custom_user()

        if grant_permission:
            grant_permissions_custom_group("can_edit_user")
            assert user.has_perm("core.can_edit_user")
        else:
            assert not user.has_perm("core.can_edit_user")

        common_user = create_user(
            email="commonuser@test.com", first_name="Common", last_name="User"
        )

        url = reverse("management:user_change_names", args=(common_user.id,))
        post_data = {"firstName": "John", "lastName": "Doe"}
        response = inertia_client.post(
            url, data=post_data, content_type="application/json"
        )

        common_user = core_models.CustomUser.objects.get(id=common_user.id)
        if grant_permission:
            assert response.status_code == 302
            assert response.url == reverse(
                "management:user_detail", args=(common_user.id,)
            )

            # Request to other view to see the share props
            response = inertia_client.get(response.url)
            assert response.status_code == 200

            data = response.json()

            assert data["props"]["flash"]["success"] == "Successful name change"

            # Verify names changed
            assert common_user.first_name == "John"
            assert common_user.last_name == "Doe"
        else:
            # Inertia client somehow tries to request a GET view (probably 403_error)
            assert response.status_code == 405

            # Verify names did not change
            assert common_user.first_name == "Common"
            assert common_user.last_name == "User"

    @pytest.mark.django_db
    def test_not_authenticated(self, inertia_client, create_user):
        """The response should redirect to the login URL."""
        common_user = create_user(
            email="commonuser@test.com", first_name="Common", last_name="User"
        )

        url = reverse("management:user_change_names", args=(common_user.id,))

        post_data = {"firstName": "John", "lastName": "Doe"}
        response = inertia_client.post(
            url, data=post_data, content_type="application/json"
        )
        assert response.status_code == 302
        assert response.url == "/login"


class TestUserChangeJobTitle:
    """Tests for the `user_change_job_title` view."""

    @pytest.mark.django_db
    @pytest.mark.parametrize(
        ["initial_job_title", "job_title"],
        list(product(["", "Developer", "Manager"], repeat=2)),
    )
    def test_manager(
        self,
        auto_login_manager_user,
        create_user,
        initial_job_title: str,
        job_title: str,
    ):
        """
        The response should change the user's job title and return redirect to
        user_detail.
        """
        inertia_client, user = auto_login_manager_user()
        assert user.has_perm("core.can_edit_user")

        common_user = create_user(
            email="commonuser@test.com", first_name="Common", last_name="User"
        )
        profile, created = core_models.UserProfile.objects.get_or_create(
            user=common_user
        )
        profile.job_title = initial_job_title
        profile.save()

        url = reverse("management:user_change_job_title", args=(common_user.id,))
        post_data = {"jobTitle": job_title}
        response = inertia_client.post(
            url, data=post_data, content_type="application/json"
        )
        assert response.status_code == 302
        assert response.url == reverse("management:user_detail", args=(common_user.id,))

        # Request to other view to see the share props
        response = inertia_client.get(response.url)
        assert response.status_code == 200

        data = response.json()

        profile = core_models.UserProfile.objects.get(user=common_user)

        if job_title:
            assert data["props"]["flash"]["success"] == "Successful job title change"

            # Verify job title changed
            assert profile.job_title == job_title
        else:
            assert data["props"]["flash"]["error"] == "Exists errors on form"

            # Verify job title did not change
            assert profile.job_title == initial_job_title

    @pytest.mark.django_db
    def test_manager_invalid_id(self, auto_login_manager_user):
        """The response should return error and redirect to user_list."""
        inertia_client, user = auto_login_manager_user()
        assert user.has_perm("core.can_edit_user")

        url = reverse("management:user_change_job_title", args=("3534465",))
        post_data = {"jobTitle": "Developer"}
        response = inertia_client.post(
            url, data=post_data, content_type="application/json"
        )
        assert response.status_code == 302
        assert response.url == reverse("management:users")

        # Request to other view to see the share props
        response = inertia_client.get(response.url)
        assert response.status_code == 200

        data = response.json()
        assert data["props"]["errors"] == "This user does not exist"

    @pytest.mark.django_db
    def test_client(self, auto_login_user, create_user):
        """Client user should not have permission to access the view."""
        inertia_client, user = auto_login_user()
        assert not user.has_perm("core.can_edit_user")

        common_user = create_user(
            email="commonuser@test.com", first_name="Common", last_name="User"
        )
        profile, created = core_models.UserProfile.objects.get_or_create(
            user=common_user
        )
        initial_job_title = profile.job_title

        url = reverse("management:user_change_job_title", args=(common_user.id,))
        post_data = {"jobTitle": "Developer"}
        response = inertia_client.post(
            url, data=post_data, content_type="application/json"
        )
        # Inertia client somehow tries to request a GET view (probably 403_error)
        assert response.status_code == 405

        # Verify job title did not change
        profile = core_models.UserProfile.objects.get(user=common_user)
        assert profile.job_title == initial_job_title

    @pytest.mark.django_db
    @pytest.mark.parametrize("grant_permission", [False, True])
    def test_custom(
        self,
        auto_login_custom_user,
        create_user,
        grant_permissions_custom_group,
        grant_permission: bool,
    ):
        """
        Custom users should only be able to access the view if their group
        has the required permission.
        """
        inertia_client, user = auto_login_custom_user()

        if grant_permission:
            grant_permissions_custom_group("can_edit_user")
            assert user.has_perm("core.can_edit_user")
        else:
            assert not user.has_perm("core.can_edit_user")

        common_user = create_user(
            email="commonuser@test.com", first_name="Common", last_name="User"
        )
        profile, created = core_models.UserProfile.objects.get_or_create(
            user=common_user
        )
        initial_job_title = profile.job_title

        url = reverse("management:user_change_job_title", args=(common_user.id,))
        post_data = {"jobTitle": "Developer"}
        response = inertia_client.post(
            url, data=post_data, content_type="application/json"
        )

        profile = core_models.UserProfile.objects.get(user=common_user)
        if grant_permission:
            assert response.status_code == 302
            assert response.url == reverse(
                "management:user_detail", args=(common_user.id,)
            )

            # Request to other view to see the share props
            response = inertia_client.get(response.url)
            assert response.status_code == 200

            data = response.json()

            assert data["props"]["flash"]["success"] == "Successful job title change"

            # Verify job title changed
            assert profile.job_title == "Developer"
        else:
            # Inertia client somehow tries to request a GET view (probably 403_error)
            assert response.status_code == 405

            # Verify job title did not change
            assert profile.job_title == initial_job_title

    @pytest.mark.django_db
    def test_not_authenticated(self, inertia_client, create_user):
        """The response should redirect to the login URL."""
        common_user = create_user(
            email="commonuser@test.com", first_name="Common", last_name="User"
        )
        profile, created = core_models.UserProfile.objects.get_or_create(
            user=common_user
        )
        initial_job_title = profile.job_title

        url = reverse("management:user_change_job_title", args=(common_user.id,))

        post_data = {"jobTitle": "Developer"}
        response = inertia_client.post(
            url, data=post_data, content_type="application/json"
        )
        assert response.status_code == 302
        assert response.url == "/login"

        # Verify job title did not change
        profile = core_models.UserProfile.objects.get(user=common_user)
        assert profile.job_title == initial_job_title


class TestUserChangeLanguage:
    """Tests for the `user_change_language` view."""

    @pytest.mark.django_db
    @pytest.mark.parametrize(
        ["initial_language", "language"], list(product(["", "en-us", "es"], repeat=2))
    )
    def test_manager(
        self, auto_login_manager_user, create_user, initial_language: str, language: str
    ):
        """
        The response should change the user's language and return redirect to
        user_detail.
        """
        inertia_client, user = auto_login_manager_user()
        assert user.has_perm("core.can_edit_user")

        common_user = create_user(
            email="commonuser@test.com", first_name="Common", last_name="User"
        )
        profile, created = core_models.UserProfile.objects.get_or_create(
            user=common_user
        )
        if initial_language:
            profile.language = initial_language
            profile.save()
        else:
            initial_language = profile.language

        url = reverse("management:user_change_language", args=(common_user.id,))
        post_data = {"language": language}
        response = inertia_client.post(
            url, data=post_data, content_type="application/json"
        )
        assert response.status_code == 302
        assert response.url == reverse("management:user_detail", args=(common_user.id,))

        # Request to other view to see the share props
        response = inertia_client.get(response.url)
        assert response.status_code == 200

        data = response.json()

        profile = core_models.UserProfile.objects.get(user=common_user)

        if language:
            assert data["props"]["flash"]["success"] == "Successful language change"

            # Verify language changed
            assert profile.language == language
        else:
            assert data["props"]["flash"]["error"] == "Exists errors on form"

            # Verify language did not change
            assert profile.language == initial_language

    @pytest.mark.django_db
    def test_manager_invalid_id(self, auto_login_manager_user):
        """The response should return error and redirect to user_list."""
        inertia_client, user = auto_login_manager_user()
        assert user.has_perm("core.can_edit_user")

        url = reverse("management:user_change_language", args=("3534465",))
        post_data = {"language": "es"}
        response = inertia_client.post(
            url, data=post_data, content_type="application/json"
        )
        assert response.status_code == 302
        assert response.url == reverse("management:users")

        # Request to other view to see the share props
        response = inertia_client.get(response.url)
        assert response.status_code == 200

        data = response.json()
        assert data["props"]["errors"] == "This user does not exist"

    @pytest.mark.django_db
    def test_client(self, auto_login_user, create_user):
        """Client user should not have permission to access the view."""
        inertia_client, user = auto_login_user()
        assert not user.has_perm("core.can_edit_user")

        common_user = create_user(
            email="commonuser@test.com", first_name="Common", last_name="User"
        )
        profile, created = core_models.UserProfile.objects.get_or_create(
            user=common_user
        )
        initial_language = profile.language

        url = reverse("management:user_change_language", args=(common_user.id,))
        post_data = {"language": "es"}
        response = inertia_client.post(
            url, data=post_data, content_type="application/json"
        )
        # Inertia client somehow tries to request a GET view (probably 403_error)
        assert response.status_code == 405

        # Verify language did not change
        profile = core_models.UserProfile.objects.get(user=common_user)
        assert profile.language == initial_language

    @pytest.mark.django_db
    @pytest.mark.parametrize("grant_permission", [False, True])
    def test_custom(
        self,
        auto_login_custom_user,
        create_user,
        grant_permissions_custom_group,
        grant_permission: bool,
    ):
        """
        Custom users should only be able to access the view if their group
        has the required permission.
        """
        inertia_client, user = auto_login_custom_user()

        if grant_permission:
            grant_permissions_custom_group("can_edit_user")
            assert user.has_perm("core.can_edit_user")
        else:
            assert not user.has_perm("core.can_edit_user")

        common_user = create_user(
            email="commonuser@test.com", first_name="Common", last_name="User"
        )
        profile, created = core_models.UserProfile.objects.get_or_create(
            user=common_user
        )
        initial_language = profile.language

        url = reverse("management:user_change_language", args=(common_user.id,))
        post_data = {"language": "es"}
        response = inertia_client.post(
            url, data=post_data, content_type="application/json"
        )

        profile = core_models.UserProfile.objects.get(user=common_user)
        if grant_permission:
            assert response.status_code == 302
            assert response.url == reverse(
                "management:user_detail", args=(common_user.id,)
            )

            # Request to other view to see the share props
            response = inertia_client.get(response.url)
            assert response.status_code == 200

            data = response.json()

            assert data["props"]["flash"]["success"] == "Successful language change"

            # Verify language changed
            assert profile.language == "es"
        else:
            # Inertia client somehow tries to request a GET view (probably 403_error)
            assert response.status_code == 405

            # Verify language did not change
            assert profile.language == initial_language

    @pytest.mark.django_db
    def test_not_authenticated(self, inertia_client, create_user):
        """The response should redirect to the login URL."""
        common_user = create_user(
            email="commonuser@test.com", first_name="Common", last_name="User"
        )
        profile, created = core_models.UserProfile.objects.get_or_create(
            user=common_user
        )
        initial_language = profile.language

        url = reverse("management:user_change_language", args=(common_user.id,))

        post_data = {"language": "es"}
        response = inertia_client.post(
            url, data=post_data, content_type="application/json"
        )
        assert response.status_code == 302
        assert response.url == "/login"

        # Verify language did not change
        profile = core_models.UserProfile.objects.get(user=common_user)
        assert profile.language == initial_language


class TestUserChangeCountry:
    """Tests for the `user_change_country` view."""

    @pytest.mark.django_db
    @pytest.mark.parametrize(
        ["initial_country", "country"], list(product(["", "US", "VE"], repeat=2))
    )
    def test_manager(
        self, auto_login_manager_user, create_user, initial_country: str, country: str
    ):
        """
        The response should change the user's country and return redirect to
        user_detail.
        """
        inertia_client, user = auto_login_manager_user()
        assert user.has_perm("core.can_edit_user")

        common_user = create_user(
            email="commonuser@test.com", first_name="Common", last_name="User"
        )
        profile, created = core_models.UserProfile.objects.get_or_create(
            user=common_user
        )
        profile.country = initial_country
        profile.save()

        url = reverse("management:user_change_country", args=(common_user.id,))
        post_data = {"country": country}
        response = inertia_client.post(
            url, data=post_data, content_type="application/json"
        )
        assert response.status_code == 302
        assert response.url == reverse("management:user_detail", args=(common_user.id,))

        # Request to other view to see the share props
        response = inertia_client.get(response.url)
        assert response.status_code == 200

        data = response.json()

        profile = core_models.UserProfile.objects.get(user=common_user)

        if country:
            assert data["props"]["flash"]["success"] == "Successful country change"

            # Verify country changed
            assert profile.country == country
        else:
            assert data["props"]["flash"]["error"] == "Exists errors on form"

            # Verify country did not change
            assert profile.country == initial_country

    @pytest.mark.django_db
    def test_manager_invalid_id(self, auto_login_manager_user):
        """The response should return error and redirect to user_list."""
        inertia_client, user = auto_login_manager_user()
        assert user.has_perm("core.can_edit_user")

        url = reverse("management:user_change_country", args=("3534465",))
        post_data = {"country": "VE"}
        response = inertia_client.post(
            url, data=post_data, content_type="application/json"
        )
        assert response.status_code == 302
        assert response.url == reverse("management:users")

        # Request to other view to see the share props
        response = inertia_client.get(response.url)
        assert response.status_code == 200

        data = response.json()
        assert data["props"]["errors"] == "This user does not exist"

    @pytest.mark.django_db
    def test_client(self, auto_login_user, create_user):
        """Client user should not have permission to access the view."""
        inertia_client, user = auto_login_user()
        assert not user.has_perm("core.can_edit_user")

        common_user = create_user(
            email="commonuser@test.com", first_name="Common", last_name="User"
        )
        profile, created = core_models.UserProfile.objects.get_or_create(
            user=common_user
        )
        initial_country = profile.country

        url = reverse("management:user_change_country", args=(common_user.id,))
        post_data = {"country": "VE"}
        response = inertia_client.post(
            url, data=post_data, content_type="application/json"
        )
        # Inertia client somehow tries to request a GET view (probably 403_error)
        assert response.status_code == 405

        # Verify country did not change
        profile = core_models.UserProfile.objects.get(user=common_user)
        assert profile.country == initial_country

    @pytest.mark.django_db
    @pytest.mark.parametrize("grant_permission", [False, True])
    def test_custom(
        self,
        auto_login_custom_user,
        create_user,
        grant_permissions_custom_group,
        grant_permission: bool,
    ):
        """
        Custom users should only be able to access the view if their group
        has the required permission.
        """
        inertia_client, user = auto_login_custom_user()

        if grant_permission:
            grant_permissions_custom_group("can_edit_user")
            assert user.has_perm("core.can_edit_user")
        else:
            assert not user.has_perm("core.can_edit_user")

        common_user = create_user(
            email="commonuser@test.com", first_name="Common", last_name="User"
        )
        profile, created = core_models.UserProfile.objects.get_or_create(
            user=common_user
        )
        initial_country = profile.country

        url = reverse("management:user_change_country", args=(common_user.id,))
        post_data = {"country": "VE"}
        response = inertia_client.post(
            url, data=post_data, content_type="application/json"
        )

        profile = core_models.UserProfile.objects.get(user=common_user)
        if grant_permission:
            assert response.status_code == 302
            assert response.url == reverse(
                "management:user_detail", args=(common_user.id,)
            )

            # Request to other view to see the share props
            response = inertia_client.get(response.url)
            assert response.status_code == 200

            data = response.json()

            assert data["props"]["flash"]["success"] == "Successful country change"

            # Verify country changed
            assert profile.country == "VE"
        else:
            # Inertia client somehow tries to request a GET view (probably 403_error)
            assert response.status_code == 405

            # Verify country did not change
            assert profile.country == initial_country

    @pytest.mark.django_db
    def test_not_authenticated(self, inertia_client, create_user):
        """The response should redirect to the login URL."""
        common_user = create_user(
            email="commonuser@test.com", first_name="Common", last_name="User"
        )
        profile, created = core_models.UserProfile.objects.get_or_create(
            user=common_user
        )
        initial_country = profile.country

        url = reverse("management:user_change_country", args=(common_user.id,))

        post_data = {"country": "VE"}
        response = inertia_client.post(
            url, data=post_data, content_type="application/json"
        )
        assert response.status_code == 302
        assert response.url == "/login"

        # Verify country did not change
        profile = core_models.UserProfile.objects.get(user=common_user)
        assert profile.country == initial_country


class TestUserChangeDateFormat:
    """Tests for the `user_change_date_format` view."""

    @pytest.mark.django_db
    @pytest.mark.parametrize(
        ["initial_date_format", "date_format"],
        list(product(["", "dd-mm-yyyy", "MM/DD/YY"], repeat=2)),
    )
    def test_manager(
        self,
        auto_login_manager_user,
        create_user,
        initial_date_format: str,
        date_format: str,
    ):
        """
        The response should change the user's date format and return redirect to
        user_detail.
        """
        inertia_client, user = auto_login_manager_user()
        assert user.has_perm("core.can_edit_user")

        common_user = create_user(
            email="commonuser@test.com", first_name="Common", last_name="User"
        )
        profile, created = core_models.UserProfile.objects.get_or_create(
            user=common_user
        )
        if initial_date_format:
            profile.date_format = initial_date_format
            profile.save()
        else:
            initial_date_format = "dd-mm-yyyy"

        url = reverse("management:user_change_date_format", args=(common_user.id,))
        post_data = {"dateFormat": date_format}
        response = inertia_client.post(
            url, data=post_data, content_type="application/json"
        )
        assert response.status_code == 302
        assert response.url == reverse("management:user_detail", args=(common_user.id,))

        # Request to other view to see the share props
        response = inertia_client.get(response.url)
        assert response.status_code == 200

        data = response.json()

        profile = core_models.UserProfile.objects.get(user=common_user)

        if date_format:
            assert data["props"]["flash"]["success"] == "Successful date format change"

            # Verify date format changed
            assert profile.date_format == date_format
        else:
            assert data["props"]["flash"]["error"] == "Exists errors on form"

            # Verify date format did not change
            assert profile.date_format == initial_date_format

    @pytest.mark.django_db
    def test_manager_invalid_id(self, auto_login_manager_user):
        """The response should return error and redirect to user_list."""
        inertia_client, user = auto_login_manager_user()
        assert user.has_perm("core.can_edit_user")

        url = reverse("management:user_change_date_format", args=("3534465",))
        post_data = {"dateFormat": "MM/DD/YY"}
        response = inertia_client.post(
            url, data=post_data, content_type="application/json"
        )
        assert response.status_code == 302
        assert response.url == reverse("management:users")

        # Request to other view to see the share props
        response = inertia_client.get(response.url)
        assert response.status_code == 200

        data = response.json()
        assert data["props"]["errors"] == "This user does not exist"

    @pytest.mark.django_db
    def test_client(self, auto_login_user, create_user):
        """Client user should not have permission to access the view."""
        inertia_client, user = auto_login_user()
        assert not user.has_perm("core.can_edit_user")

        common_user = create_user(
            email="commonuser@test.com", first_name="Common", last_name="User"
        )
        profile, created = core_models.UserProfile.objects.get_or_create(
            user=common_user
        )
        initial_date_format = profile.date_format

        url = reverse("management:user_change_date_format", args=(common_user.id,))
        post_data = {"dateFormat": "MM/DD/YY"}
        response = inertia_client.post(
            url, data=post_data, content_type="application/json"
        )
        # Inertia client somehow tries to request a GET view (probably 403_error)
        assert response.status_code == 405

        # Verify date format did not change
        profile = core_models.UserProfile.objects.get(user=common_user)
        assert profile.date_format == initial_date_format

    @pytest.mark.django_db
    @pytest.mark.parametrize("grant_permission", [False, True])
    def test_custom(
        self,
        auto_login_custom_user,
        create_user,
        grant_permissions_custom_group,
        grant_permission: bool,
    ):
        """
        Custom users should only be able to access the view if their group
        has the required permission.
        """
        inertia_client, user = auto_login_custom_user()

        if grant_permission:
            grant_permissions_custom_group("can_edit_user")
            assert user.has_perm("core.can_edit_user")
        else:
            assert not user.has_perm("core.can_edit_user")

        common_user = create_user(
            email="commonuser@test.com", first_name="Common", last_name="User"
        )
        profile, created = core_models.UserProfile.objects.get_or_create(
            user=common_user
        )
        initial_date_format = profile.date_format

        url = reverse("management:user_change_date_format", args=(common_user.id,))
        post_data = {"dateFormat": "MM/DD/YY"}
        response = inertia_client.post(
            url, data=post_data, content_type="application/json"
        )

        profile = core_models.UserProfile.objects.get(user=common_user)
        if grant_permission:
            assert response.status_code == 302
            assert response.url == reverse(
                "management:user_detail", args=(common_user.id,)
            )

            # Request to other view to see the share props
            response = inertia_client.get(response.url)
            assert response.status_code == 200

            data = response.json()

            assert data["props"]["flash"]["success"] == "Successful date format change"

            # Verify date format changed
            assert profile.date_format == "MM/DD/YY"
        else:
            # Inertia client somehow tries to request a GET view (probably 403_error)
            assert response.status_code == 405

            # Verify date format did not change
            assert profile.date_format == initial_date_format

    @pytest.mark.django_db
    def test_not_authenticated(self, inertia_client, create_user):
        """The response should redirect to the login URL."""
        common_user = create_user(
            email="commonuser@test.com", first_name="Common", last_name="User"
        )
        profile, created = core_models.UserProfile.objects.get_or_create(
            user=common_user
        )
        initial_date_format = profile.date_format

        url = reverse("management:user_change_date_format", args=(common_user.id,))

        post_data = {"dateFormat": "MM/DD/YY"}
        response = inertia_client.post(
            url, data=post_data, content_type="application/json"
        )
        assert response.status_code == 302
        assert response.url == "/login"

        # Verify date format did not change
        profile = core_models.UserProfile.objects.get(user=common_user)
        assert profile.date_format == initial_date_format


class TestUserChangePhoto:
    """Tests for the `user_change_photo` view."""

    @pytest.mark.django_db
    def test_manager(self, auto_login_manager_user, create_user, test_image_file):
        """
        The response should change the user's photo and return redirect to
        user_detail.
        """
        inertia_client, user = auto_login_manager_user()
        assert user.has_perm("core.can_edit_user")

        common_user = create_user(
            email="commonuser@test.com", first_name="Common", last_name="User"
        )
        profile, created = core_models.UserProfile.objects.get_or_create(
            user=common_user
        )
        assert not profile.photo

        url = reverse("management:user_change_photo", args=(common_user.id,))
        post_data = {"photo": test_image_file}
        response = inertia_client.post(
            url, data=post_data, content_type=MULTIPART_CONTENT
        )

        assert response.status_code == 302
        assert response.url == reverse("management:user_detail", args=(common_user.id,))

        # Request to other view to see the share props
        response = inertia_client.get(response.url)
        assert response.status_code == 200

        data = response.json()

        assert data["props"]["flash"]["success"] == "Successful photo change"

        profile = core_models.UserProfile.objects.filter(user=common_user).first()
        assert profile is not None
        assert profile.photo
        assert profile.get_photo().startswith("data:image/png;base64,")

    @pytest.mark.django_db
    @pytest.mark.parametrize("mode", ["invalid_file", "no_data"])
    def test_manager_invalid(self, auto_login_manager_user, create_user, mode: str):
        """
        The response should show error and return redirect to
        user_detail.
        """
        inertia_client, user = auto_login_manager_user()
        assert user.has_perm("core.can_edit_user")

        common_user = create_user(
            email="commonuser@test.com", first_name="Common", last_name="User"
        )
        profile, created = core_models.UserProfile.objects.get_or_create(
            user=common_user
        )
        assert not profile.photo

        url = reverse("management:user_change_photo", args=(common_user.id,))
        if mode == "invalid_file":
            post_data = {
                "photo": ("photo.jpg", io.BytesIO(b"some random data"), "image/jpg")
            }
        else:
            post_data = {}
        response = inertia_client.post(
            url, data=post_data, content_type=MULTIPART_CONTENT
        )

        assert response.status_code == 302
        assert response.url == reverse("management:user_detail", args=(common_user.id,))

        # Request to other view to see the share props
        response = inertia_client.get(response.url)
        assert response.status_code == 200

        data = response.json()

        profile = core_models.UserProfile.objects.filter(user=common_user).first()
        assert profile is not None
        assert not profile.photo

        assert data["props"]["flash"]["error"] == "Exists errors on form"
        assert data["props"]["errors"]

        if mode == "invalid_file":
            assert data["props"]["errors"]["photo"] == [
                "Invalid file type, please choose another one."
            ]
        else:
            assert data["props"]["errors"]["photo"] == ["This field is required."]

    @pytest.mark.django_db
    def test_manager_invalid_id(self, auto_login_manager_user, test_image_file):
        """The response should show error and return redirect to users."""
        inertia_client, user = auto_login_manager_user()
        assert user.has_perm("core.can_edit_user")

        url = reverse("management:user_change_photo", args=("1234",))
        post_data = {"logo": test_image_file}
        response = inertia_client.post(
            url, data=post_data, content_type=MULTIPART_CONTENT
        )

        assert response.status_code == 302
        assert response.url == reverse("management:users")

        # Request to other view to see the share props
        response = inertia_client.get(response.url)
        assert response.status_code == 200

        data = response.json()

        assert data["props"]["flash"]["error"]
        assert data["props"]["errors"] == "This user does not exist"

    @pytest.mark.django_db
    def test_client(self, auto_login_user, create_user, test_image_file):
        """Client user should not have permission to access the view."""
        inertia_client, user = auto_login_user()
        assert not user.has_perm("core.can_edit_user")

        common_user = create_user(
            email="commonuser@test.com", first_name="Common", last_name="User"
        )
        profile, created = core_models.UserProfile.objects.get_or_create(
            user=common_user
        )
        assert not profile.photo

        url = reverse("management:user_change_photo", args=(common_user.id,))
        post_data = {"photo": test_image_file}
        response = inertia_client.post(
            url, data=post_data, content_type=MULTIPART_CONTENT
        )

        # Inertia client somehow tries to request a GET view (probably 403_error)
        assert response.status_code == 405

        profile = core_models.UserProfile.objects.filter(user=common_user).first()
        assert profile is not None
        assert not profile.photo

    @pytest.mark.django_db
    @pytest.mark.parametrize("grant_permission", [False, True])
    def test_custom(
        self,
        auto_login_custom_user,
        create_user,
        test_image_file,
        grant_permissions_custom_group,
        grant_permission: bool,
    ):
        """
        Custom users should only be able to access the view if their group
        has the required permission.
        """
        inertia_client, user = auto_login_custom_user()

        if grant_permission:
            grant_permissions_custom_group("can_edit_user")
            assert user.has_perm("core.can_edit_user")
        else:
            assert not user.has_perm("core.can_edit_user")

        common_user = create_user(
            email="commonuser@test.com", first_name="Common", last_name="User"
        )
        profile, created = core_models.UserProfile.objects.get_or_create(
            user=common_user
        )
        assert not profile.photo

        url = reverse("management:user_change_photo", args=(common_user.id,))
        post_data = {"photo": test_image_file}
        response = inertia_client.post(
            url, data=post_data, content_type=MULTIPART_CONTENT
        )

        profile = core_models.UserProfile.objects.filter(user=common_user).first()
        assert profile is not None

        if grant_permission:
            assert response.status_code == 302
            assert response.url == reverse(
                "management:user_detail", args=(common_user.id,)
            )

            # Request to other view to see the share props
            response = inertia_client.get(response.url)
            assert response.status_code == 200

            data = response.json()
            assert data["props"]["flash"]["success"] == "Successful photo change"

            assert profile.photo
            assert profile.get_photo().startswith("data:image/png;base64,")
        else:
            # Inertia client somehow tries to request a GET view (probably 403_error)
            assert response.status_code == 405

            assert not profile.photo

    @pytest.mark.django_db
    def test_not_authenticated(self, inertia_client, create_user, test_image_file):
        """The response should redirect to the login URL."""
        common_user = create_user(
            email="commonuser@test.com", first_name="Common", last_name="User"
        )
        profile, created = core_models.UserProfile.objects.get_or_create(
            user=common_user
        )
        assert not profile.photo

        url = reverse("management:user_change_photo", args=(common_user.id,))
        post_data = {"photo": test_image_file}
        response = inertia_client.post(
            url, data=post_data, content_type=MULTIPART_CONTENT
        )

        assert response.status_code == 302
        assert response.url == "/login"

        profile = core_models.UserProfile.objects.filter(user=common_user).first()
        assert profile is not None
        assert not profile.photo


class TestUserRemovePhoto:
    """Tests for the `user_remove_photo` view."""

    @pytest.mark.django_db
    def test_manager(self, auto_login_manager_user, create_user, test_image_file):
        """
        The response should remove the user's photo and return redirect to
        user_detail.
        """
        inertia_client, user = auto_login_manager_user()
        assert user.has_perm("core.can_edit_user")

        common_user = create_user(
            email="commonuser@test.com", first_name="Common", last_name="User"
        )
        profile, created = core_models.UserProfile.objects.update_or_create(
            user=common_user, defaults={"photo": test_image_file}
        )
        assert profile.photo
        assert profile.get_photo().startswith("data:image/png;base64,")

        url = reverse("management:user_remove_photo", args=(common_user.id,))
        response = inertia_client.get(url)

        assert response.status_code == 302
        assert response.url == reverse("management:user_detail", args=(common_user.id,))

        # Request to other view to see the share props
        response = inertia_client.get(response.url)
        assert response.status_code == 200

        data = response.json()

        assert data["props"]["flash"]["success"] == "Photo successfully removed"

        profile = core_models.UserProfile.objects.filter(user=common_user).first()
        assert profile is not None
        assert not profile.photo

    @pytest.mark.django_db
    def test_manager_invalid_id(self, auto_login_manager_user):
        """The response should show error and return redirect to users."""
        inertia_client, user = auto_login_manager_user()
        assert user.has_perm("core.can_edit_user")

        url = reverse("management:user_remove_photo", args=("1234",))
        response = inertia_client.get(url)

        assert response.status_code == 302
        assert response.url == reverse("management:users")

        # Request to other view to see the share props
        response = inertia_client.get(response.url)
        assert response.status_code == 200

        data = response.json()

        assert data["props"]["flash"]["error"]
        assert data["props"]["errors"] == "This user does not exist"

    @pytest.mark.django_db
    def test_client(self, auto_login_user, create_user, test_image_file):
        """Client user should not have permission to access the view."""
        inertia_client, user = auto_login_user()
        assert not user.has_perm("core.can_edit_user")

        common_user = create_user(
            email="commonuser@test.com", first_name="Common", last_name="User"
        )
        profile, created = core_models.UserProfile.objects.update_or_create(
            user=common_user, defaults={"photo": test_image_file}
        )
        assert profile.photo
        assert profile.get_photo().startswith("data:image/png;base64,")

        url = reverse("management:user_remove_photo", args=(common_user.id,))
        response = inertia_client.get(url)

        assert response.status_code == 200

        data = response.json()
        assert data["component"] == "403Error"

        profile = core_models.UserProfile.objects.filter(user=common_user).first()
        assert profile is not None
        assert profile.photo

    @pytest.mark.django_db
    @pytest.mark.parametrize("grant_permission", [False, True])
    def test_custom(
        self,
        auto_login_custom_user,
        create_user,
        test_image_file,
        grant_permissions_custom_group,
        grant_permission: bool,
    ):
        """
        Custom users should only be able to access the view if their group
        has the required permission.
        """
        inertia_client, user = auto_login_custom_user()

        if grant_permission:
            grant_permissions_custom_group("can_edit_user")
            assert user.has_perm("core.can_edit_user")
        else:
            assert not user.has_perm("core.can_edit_user")

        common_user = create_user(
            email="commonuser@test.com", first_name="Common", last_name="User"
        )
        profile, created = core_models.UserProfile.objects.update_or_create(
            user=common_user, defaults={"photo": test_image_file}
        )
        assert profile.photo
        assert profile.get_photo().startswith("data:image/png;base64,")

        url = reverse("management:user_remove_photo", args=(common_user.id,))
        response = inertia_client.get(url)

        profile = core_models.UserProfile.objects.filter(user=common_user).first()
        assert profile is not None

        if grant_permission:
            assert response.status_code == 302
            assert response.url == reverse(
                "management:user_detail", args=(common_user.id,)
            )

            # Request to other view to see the share props
            response = inertia_client.get(response.url)
            assert response.status_code == 200

            data = response.json()
            assert data["props"]["flash"]["success"] == "Photo successfully removed"

            assert not profile.photo
        else:
            assert response.status_code == 200

            data = response.json()
            assert data["component"] == "403Error"

            assert profile.photo

    @pytest.mark.django_db
    def test_not_authenticated(self, inertia_client, create_user, test_image_file):
        """The response should redirect to the login URL."""
        common_user = create_user(
            email="commonuser@test.com", first_name="Common", last_name="User"
        )
        profile, created = core_models.UserProfile.objects.update_or_create(
            user=common_user, defaults={"photo": test_image_file}
        )
        assert profile.photo

        url = reverse("management:user_remove_photo", args=(common_user.id,))
        response = inertia_client.get(url)

        assert response.status_code == 302
        assert response.url == "/login"

        profile = core_models.UserProfile.objects.filter(user=common_user).first()
        assert profile is not None
        assert profile.photo


class TestUserChangeGroups:
    """Tests for the `change_user_groups` view."""

    @pytest.mark.django_db
    @pytest.mark.parametrize("group", ["", "management", "custom"])
    def test_manager(self, auto_login_manager_user, create_user, group: str):
        """
        The response should change the user's group and return redirect to
        user_detail.
        """
        inertia_client, user = auto_login_manager_user()
        assert user.has_perm("core.can_edit_user")

        common_user = create_user(
            email="commonuser@test.com", first_name="Common", last_name="User"
        )
        assert common_user.groups.count() == 1
        assert common_user.groups.first().name == "customer"

        url = reverse("management:change_user_groups", args=(common_user.id,))
        post_data = {"group": group}
        response = inertia_client.post(
            url, data=post_data, content_type="application/json"
        )
        assert response.status_code == 302
        assert response.url == reverse("management:user_detail", args=(common_user.id,))

        # Request to other view to see the share props
        response = inertia_client.get(response.url)
        assert response.status_code == 200

        data = response.json()

        common_user = core_models.CustomUser.objects.get(id=common_user.id)

        if group and Group.objects.filter(name=group).exists():
            assert data["props"]["flash"]["success"] == "Successful role change"

            # Verify group changed
            assert common_user.groups.count() == 1
            assert common_user.groups.first().name == group
        else:
            assert data["props"]["flash"]["error"] == "Exists errors on form"

            # Verify group did not change
            assert common_user.groups.count() == 1
            assert common_user.groups.first().name == "customer"

    @pytest.mark.django_db
    def test_manager_invalid_id(self, auto_login_manager_user):
        """The response should return error and redirect to user_list."""
        inertia_client, user = auto_login_manager_user()
        assert user.has_perm("core.can_edit_user")

        url = reverse("management:change_user_groups", args=("3534465",))
        post_data = {"group": "management"}
        response = inertia_client.post(
            url, data=post_data, content_type="application/json"
        )
        assert response.status_code == 302
        assert response.url == reverse("management:users")

        # Request to other view to see the share props
        response = inertia_client.get(response.url)
        assert response.status_code == 200

        data = response.json()
        assert data["props"]["errors"] == "This user does not exist"

    @pytest.mark.django_db
    def test_client(self, auto_login_user, create_user):
        """Client user should not have permission to access the view."""
        inertia_client, user = auto_login_user()
        assert not user.has_perm("core.can_edit_user")

        common_user = create_user(
            email="commonuser@test.com", first_name="Common", last_name="User"
        )
        assert common_user.groups.count() == 1
        assert common_user.groups.first().name == "customer"

        url = reverse("management:change_user_groups", args=(common_user.id,))
        post_data = {"group": "management"}
        response = inertia_client.post(
            url, data=post_data, content_type="application/json"
        )
        # Inertia client somehow tries to request a GET view (probably 403_error)
        assert response.status_code == 405

        # Verify group did not change
        common_user = core_models.CustomUser.objects.get(id=common_user.id)
        assert common_user.groups.count() == 1
        assert common_user.groups.first().name == "customer"

    @pytest.mark.django_db
    @pytest.mark.parametrize("grant_permission", [False, True])
    def test_custom(
        self,
        auto_login_custom_user,
        create_user,
        grant_permissions_custom_group,
        grant_permission: bool,
    ):
        """
        Custom users should only be able to access the view if their group
        has the required permission.
        """
        inertia_client, user = auto_login_custom_user()

        if grant_permission:
            grant_permissions_custom_group("can_edit_user")
            assert user.has_perm("core.can_edit_user")
        else:
            assert not user.has_perm("core.can_edit_user")

        common_user = create_user(
            email="commonuser@test.com", first_name="Common", last_name="User"
        )
        assert common_user.groups.count() == 1
        assert common_user.groups.first().name == "customer"

        url = reverse("management:change_user_groups", args=(common_user.id,))
        post_data = {"group": "management"}
        response = inertia_client.post(
            url, data=post_data, content_type="application/json"
        )

        common_user = core_models.CustomUser.objects.get(id=common_user.id)
        if grant_permission:
            assert response.status_code == 302
            assert response.url == reverse(
                "management:user_detail", args=(common_user.id,)
            )

            # Request to other view to see the share props
            response = inertia_client.get(response.url)
            assert response.status_code == 200

            data = response.json()

            assert data["props"]["flash"]["success"] == "Successful role change"

            # Verify group changed
            assert common_user.groups.count() == 1
            assert common_user.groups.first().name == "management"
        else:
            # Inertia client somehow tries to request a GET view (probably 403_error)
            assert response.status_code == 405

            # Verify group did not change
            assert common_user.groups.count() == 1
            assert common_user.groups.first().name == "customer"

    @pytest.mark.django_db
    def test_not_authenticated(self, inertia_client, create_user):
        """The response should redirect to the login URL."""
        common_user = create_user(
            email="commonuser@test.com", first_name="Common", last_name="User"
        )
        assert common_user.groups.count() == 1
        assert common_user.groups.first().name == "customer"

        url = reverse("management:change_user_groups", args=(common_user.id,))

        post_data = {"group": "management"}
        response = inertia_client.post(
            url, data=post_data, content_type="application/json"
        )
        assert response.status_code == 302
        assert response.url == "/login"


class TestUserCreate:
    """Tests for the `create_user` view."""

    @pytest.mark.django_db
    def test_manager_get(self, auto_login_manager_user):
        """The response should return the UserCreate component and props."""
        inertia_client, user = auto_login_manager_user()
        assert user.has_perm("core.can_create_user")

        url = reverse("management:user_create")
        response = inertia_client.get(url)
        assert response.status_code == 200

        data = response.json()
        assert data["component"] == "UserCreate"
        assert "availableGroups" in data["props"]

    @pytest.mark.django_db
    @pytest.mark.parametrize(
        ["email", "first_name", "last_name", "group"],
        list(
            product(
                ["", "invalidemail", "commonuser@test.com", "newuser@test.com"],
                ["", "New"],
                ["", "User"],
                ["", "invalidgroup", "customer", "management"],
            )
        ),
    )
    @mock.patch("apps.accounts.tasks.email_password_reset")
    def test_manager_post(
        self,
        mock_email_confirm,
        auto_login_manager_user,
        create_user,
        email: str,
        first_name: str,
        last_name: str,
        group: str,
    ):
        """The response should create user and return redirect to user_list."""
        mock_email_confirm.return_value = True
        inertia_client, user = auto_login_manager_user()
        assert user.has_perm("core.can_create_user")

        common_user = create_user(
            email="commonuser@test.com", first_name="Common", last_name="User"
        )

        url = reverse("management:user_create")
        post_data = {
            "email": email,
            "firstName": first_name,
            "lastName": last_name,
            "group": group,
        }
        response = inertia_client.post(
            url, data=post_data, content_type="application/json"
        )

        is_email_ok = email not in ["invalidemail", common_user.email]
        is_group_ok = Group.objects.filter(name=group).exists()
        # TODO: CreateUserSchema serializer allows empty values for first and last name
        # Fix and then replace if with this:
        # if email and first_name and last_name and is_email_ok and is_group_ok:
        if email and is_email_ok and is_group_ok:
            assert response.status_code == 302
            assert response.url == reverse("management:users")

            # Request to other view to see the share props
            response = inertia_client.get(response.url)
            assert response.status_code == 200

            data = response.json()

            # TODO: Show success message
            assert not data["props"]["flash"]["error"]

            assert core_models.CustomUser.objects.filter(email=email).exists()
        else:
            assert response.status_code == 200

            data = response.json()

            error_msg = data["props"]["flash"]["error"]
            if error_msg == "User already exist":
                assert email == common_user.email
            else:
                assert error_msg == "Exists errors on form"

            if email != common_user.email:
                assert not core_models.CustomUser.objects.filter(email=email).exists()

    @pytest.mark.django_db
    def test_client_get(self, auto_login_user):
        """Client user should not have permission to access the view."""
        inertia_client, user = auto_login_user()
        assert not user.has_perm("core.can_create_user")

        url = reverse("management:user_create")
        response = inertia_client.get(url)
        assert response.status_code == 200

        data = response.json()
        assert data["component"] == "403Error"

    @pytest.mark.django_db
    def test_client_post(self, auto_login_user):
        """Client user should not have permission to access the view."""
        inertia_client, user = auto_login_user()
        assert not user.has_perm("core.can_create_user")

        url = reverse("management:user_create")
        post_data = {
            "email": "newuser@test.com",
            "firstName": "New",
            "lastName": "User",
            "group": "customer",
        }
        response = inertia_client.post(
            url, data=post_data, content_type="application/json"
        )
        # Inertia client somehow tries to request a GET view (probably 403_error)
        assert response.status_code == 405

        # Verify user not created
        assert not core_models.CustomUser.objects.filter(
            email=post_data["email"]
        ).exists()

    @pytest.mark.django_db
    @pytest.mark.parametrize("grant_permission", [False, True])
    def test_custom_get(
        self,
        auto_login_custom_user,
        grant_permissions_custom_group,
        grant_permission: bool,
    ):
        """
        Custom users should only be able to access the view if their group
        has the required permission.
        """
        inertia_client, user = auto_login_custom_user()

        if grant_permission:
            grant_permissions_custom_group("can_create_user")
            assert user.has_perm("core.can_create_user")
        else:
            assert not user.has_perm("core.can_create_user")

        url = reverse("management:user_create")
        response = inertia_client.get(url)
        assert response.status_code == 200

        data = response.json()
        if grant_permission:
            assert data["component"] == "UserCreate"
            assert "availableGroups" in data["props"]
        else:
            assert data["component"] == "403Error"

    @pytest.mark.django_db
    @pytest.mark.parametrize("grant_permission", [False, True])
    @mock.patch("apps.accounts.tasks.email_password_reset")
    def test_custom_post(
        self,
        mock_email_confirm,
        auto_login_custom_user,
        grant_permissions_custom_group,
        grant_permission: bool,
    ):
        """
        Custom users should only be able to access the view if their group
        has the required permission.
        """
        mock_email_confirm.return_value = True
        inertia_client, user = auto_login_custom_user()

        if grant_permission:
            grant_permissions_custom_group("can_create_user")
            assert user.has_perm("core.can_create_user")
        else:
            assert not user.has_perm("core.can_create_user")

        url = reverse("management:user_create")
        post_data = {
            "email": "newuser@test.com",
            "firstName": "New",
            "lastName": "User",
            "group": "customer",
        }
        response = inertia_client.post(
            url, data=post_data, content_type="application/json"
        )

        if grant_permission:
            assert response.status_code == 302
            assert response.url == reverse("management:users")

            # Request to other view to see the share props
            response = inertia_client.get(response.url)
            assert response.status_code == 200

            data = response.json()

            # TODO: Show success message
            assert not data["props"]["flash"]["error"]

            assert core_models.CustomUser.objects.filter(
                email=post_data["email"]
            ).exists()
        else:
            # Inertia client somehow tries to request a GET view (probably 403_error)
            assert response.status_code == 405

            # Verify user not created
            assert not core_models.CustomUser.objects.filter(
                email=post_data["email"]
            ).exists()

    @pytest.mark.django_db
    def test_not_authenticated_get(self, inertia_client):
        """The response should redirect to the login URL."""
        url = reverse("management:user_create")

        response = inertia_client.get(url)
        assert response.status_code == 302
        assert response.url == "/login"

    @pytest.mark.django_db
    def test_not_authenticated_post(self, inertia_client):
        """The response should redirect to the login URL."""
        url = reverse("management:user_create")

        post_data = {
            "email": "newuser@test.com",
            "firstName": "New",
            "lastName": "User",
            "group": "customer",
        }
        response = inertia_client.post(
            url, data=post_data, content_type="application/json"
        )
        assert response.status_code == 302
        assert response.url == "/login"

        # Verify user not created
        assert not core_models.CustomUser.objects.filter(
            email=post_data["email"]
        ).exists()


class TestGlobalSettingsGeneral:
    """Tests for the `global_settings_general` view."""

    @pytest.mark.django_db
    def test_manager(self, auto_login_manager_user):
        """The response should return the SystemSettingsGeneral component and props."""
        inertia_client, user = auto_login_manager_user()
        assert user.has_perm("core.can_management_global_settings")

        url = reverse("management:global_settings_general")
        response = inertia_client.get(url)
        assert response.status_code == 200

        data = response.json()
        assert data["component"] == "SystemSettingsGeneral"

    @pytest.mark.django_db
    def test_client(self, auto_login_user):
        """Client user should not have permission to access the view."""
        inertia_client, user = auto_login_user()
        assert not user.has_perm("core.can_management_global_settings")

        url = reverse("management:global_settings_general")
        response = inertia_client.get(url)
        assert response.status_code == 200

        data = response.json()
        assert data["component"] == "403Error"

    @pytest.mark.django_db
    @pytest.mark.parametrize("grant_permission", [False, True])
    def test_custom(
        self,
        auto_login_custom_user,
        grant_permissions_custom_group,
        grant_permission: bool,
    ):
        """
        Custom users should only be able to access the view if their group
        has the required permission.
        """
        inertia_client, user = auto_login_custom_user()

        if grant_permission:
            grant_permissions_custom_group("can_management_global_settings")
            assert user.has_perm("core.can_management_global_settings")
        else:
            assert not user.has_perm("core.can_management_global_settings")

        url = reverse("management:global_settings_general")
        response = inertia_client.get(url)
        assert response.status_code == 200

        data = response.json()
        if grant_permission:
            assert data["component"] == "SystemSettingsGeneral"
        else:
            assert data["component"] == "403Error"

    @pytest.mark.django_db
    def test_not_authenticated(self, inertia_client):
        """The response should redirect to the login URL."""
        url = reverse("management:global_settings_general")

        response = inertia_client.get(url)
        assert response.status_code == 302
        assert response.url == "/login"


class TestGlobalSettingsSecurity:
    """Tests for the `global_settings_security` view."""

    @pytest.mark.django_db
    def test_manager(self, auto_login_manager_user):
        """The response should return the SystemSettingsSecurity component and props."""
        inertia_client, user = auto_login_manager_user()
        assert user.has_perm("core.can_management_global_settings")

        url = reverse("management:global_settings_security")
        response = inertia_client.get(url)
        assert response.status_code == 200

        data = response.json()
        assert data["component"] == "SystemSettingsSecurity"
        assert "auditInstalled" in data["props"]

    @pytest.mark.django_db
    def test_client(self, auto_login_user):
        """Client user should not have permission to access the view."""
        inertia_client, user = auto_login_user()
        assert not user.has_perm("core.can_management_global_settings")

        url = reverse("management:global_settings_security")
        response = inertia_client.get(url)
        assert response.status_code == 200

        data = response.json()
        assert data["component"] == "403Error"

    @pytest.mark.django_db
    @pytest.mark.parametrize("grant_permission", [False, True])
    def test_custom(
        self,
        auto_login_custom_user,
        grant_permissions_custom_group,
        grant_permission: bool,
    ):
        """
        Custom users should only be able to access the view if their group
        has the required permission.
        """
        inertia_client, user = auto_login_custom_user()

        if grant_permission:
            grant_permissions_custom_group("can_management_global_settings")
            assert user.has_perm("core.can_management_global_settings")
        else:
            assert not user.has_perm("core.can_management_global_settings")

        url = reverse("management:global_settings_security")
        response = inertia_client.get(url)
        assert response.status_code == 200

        data = response.json()
        if grant_permission:
            assert data["component"] == "SystemSettingsSecurity"
            assert "auditInstalled" in data["props"]
        else:
            assert data["component"] == "403Error"

    @pytest.mark.django_db
    def test_not_authenticated(self, inertia_client):
        """The response should redirect to the login URL."""
        url = reverse("management:global_settings_security")

        response = inertia_client.get(url)
        assert response.status_code == 302
        assert response.url == "/login"


class TestGlobalSettingsScripts:
    """Tests for the `global_settings_scripts` view."""

    @pytest.mark.django_db
    def test_manager_get(self, auto_login_manager_user):
        """The response should return the SystemSettingsScripts component and props."""
        inertia_client, user = auto_login_manager_user()
        assert user.has_perm("core.can_management_global_settings")

        url = reverse("management:global_settings_scripts")
        response = inertia_client.get(url)
        assert response.status_code == 200

        data = response.json()
        assert data["component"] == "SystemSettingsScripts"
        assert "header" in data["props"]
        assert "footer" in data["props"]
        assert "body" in data["props"]

        global_settings = core_models.GlobalSettings.objects.first()
        assert global_settings is not None
        if global_settings.header_scripts:
            assert data["props"]["header"] == global_settings.header_scripts
        else:
            assert data["props"]["header"] == ""
        if global_settings.footer_scripts:
            assert data["props"]["footer"] == global_settings.footer_scripts
        else:
            assert data["props"]["footer"] == ""
        if global_settings.body_scripts:
            assert data["props"]["body"] == global_settings.body_scripts
        else:
            assert data["props"]["body"] == ""

    @pytest.mark.django_db
    @pytest.mark.parametrize(
        ["header", "footer", "body"],
        list(
            product(
                ["", "header script"],
                ["", "footer script"],
                ["", "body script"],
            )
        ),
    )
    def test_manager_post(
        self, auto_login_manager_user, header: str, footer: str, body: str
    ):
        """
        The response should set scripts and return the SystemSettingsScripts
        component and props.
        """
        inertia_client, user = auto_login_manager_user()
        assert user.has_perm("core.can_management_global_settings")

        url = reverse("management:global_settings_scripts")
        post_data = {"header": header, "footer": footer, "body": body}
        response = inertia_client.post(
            url, data=post_data, content_type="application/json"
        )

        assert response.status_code == 200

        data = response.json()

        assert data["props"]["flash"]["success"] == "Scripts saved successfully"

        global_settings = core_models.GlobalSettings.objects.first()
        assert global_settings is not None
        assert global_settings.header_scripts == header
        assert global_settings.footer_scripts == footer
        assert global_settings.body_scripts == body

    @pytest.mark.django_db
    def test_manager_post_no_data(self, auto_login_manager_user):
        """
        The response should show error message and return the
        SystemSettingsScripts component and props.
        """
        inertia_client, user = auto_login_manager_user()
        assert user.has_perm("core.can_management_global_settings")

        url = reverse("management:global_settings_scripts")
        response = inertia_client.post(url, data={}, content_type="application/json")

        assert response.status_code == 200

        data = response.json()

        assert data["component"] == "SystemSettingsScripts"
        assert data["props"]["flash"]["error"] == "Exists errors on form"

        assert core_models.GlobalSettings.objects.exists()

    @pytest.mark.django_db
    def test_client_get(self, auto_login_user):
        """Client user should not have permission to access the view."""
        inertia_client, user = auto_login_user()
        assert not user.has_perm("core.can_management_global_settings")

        url = reverse("management:global_settings_scripts")
        response = inertia_client.get(url)
        assert response.status_code == 200

        data = response.json()
        assert data["component"] == "403Error"

    @pytest.mark.django_db
    def test_client_post(self, auto_login_user):
        """Client user should not have permission to access the view."""
        inertia_client, user = auto_login_user()
        assert not user.has_perm("core.can_management_global_settings")

        url = reverse("management:global_settings_scripts")
        post_data = {
            "header": "header script",
            "footer": "footer script",
            "body": "body script",
        }
        response = inertia_client.post(
            url, data=post_data, content_type="application/json"
        )
        # Inertia client somehow tries to request a GET view (probably 403_error)
        assert response.status_code == 405

        assert not core_models.GlobalSettings.objects.exists()

    @pytest.mark.django_db
    @pytest.mark.parametrize("grant_permission", [False, True])
    def test_custom_get(
        self,
        auto_login_custom_user,
        grant_permissions_custom_group,
        grant_permission: bool,
    ):
        """
        Custom users should only be able to access the view if their group
        has the required permission.
        """
        inertia_client, user = auto_login_custom_user()

        if grant_permission:
            grant_permissions_custom_group("can_management_global_settings")
            assert user.has_perm("core.can_management_global_settings")
        else:
            assert not user.has_perm("core.can_management_global_settings")

        url = reverse("management:global_settings_scripts")
        response = inertia_client.get(url)
        assert response.status_code == 200

        data = response.json()
        if grant_permission:
            assert data["component"] == "SystemSettingsScripts"
        else:
            assert data["component"] == "403Error"

    @pytest.mark.django_db
    @pytest.mark.parametrize("grant_permission", [False, True])
    def test_custom_post(
        self,
        auto_login_custom_user,
        grant_permissions_custom_group,
        grant_permission: bool,
    ):
        """
        Custom users should only be able to access the view if their group
        has the required permission.
        """
        inertia_client, user = auto_login_custom_user()

        if grant_permission:
            grant_permissions_custom_group("can_management_global_settings")
            assert user.has_perm("core.can_management_global_settings")
        else:
            assert not user.has_perm("core.can_management_global_settings")

        url = reverse("management:global_settings_scripts")
        post_data = {
            "header": "header script",
            "footer": "footer script",
            "body": "body script",
        }
        response = inertia_client.post(
            url, data=post_data, content_type="application/json"
        )

        if grant_permission:
            assert response.status_code == 200

            data = response.json()

            assert data["props"]["flash"]["success"] == "Scripts saved successfully"

            global_settings = core_models.GlobalSettings.objects.first()
            assert global_settings is not None
            assert global_settings.header_scripts == post_data["header"]
            assert global_settings.footer_scripts == post_data["footer"]
            assert global_settings.body_scripts == post_data["body"]
        else:
            # Inertia client somehow tries to request a GET view (probably 403_error)
            assert response.status_code == 405

            assert not core_models.GlobalSettings.objects.exists()

    @pytest.mark.django_db
    def test_not_authenticated_get(self, inertia_client):
        """The response should redirect to the login URL."""
        url = reverse("management:global_settings_scripts")

        response = inertia_client.get(url)
        assert response.status_code == 302
        assert response.url == "/login"

    @pytest.mark.django_db
    def test_not_authenticated_post(self, inertia_client):
        """The response should redirect to the login URL."""
        url = reverse("management:global_settings_scripts")

        post_data = {
            "header": "header script",
            "footer": "footer script",
            "body": "body script",
        }
        response = inertia_client.post(
            url, data=post_data, content_type="application/json"
        )
        assert response.status_code == 302
        assert response.url == "/login"


class TestSystemChangeAppName:
    """Tests for the `system_change_app_name` view."""

    @pytest.mark.django_db
    @pytest.mark.parametrize(
        ["create_global_settings", "app_name"],
        list(product([False, True], ["", "New app name"])),
    )
    def test_manager(
        self, auto_login_manager_user, create_global_settings: bool, app_name: str
    ):
        """
        The response should change app name and return redirect to
        global_settings_general.
        """
        inertia_client, user = auto_login_manager_user()
        assert user.has_perm("core.can_management_global_settings")

        assert not core_models.GlobalSettings.objects.exists()
        if create_global_settings:
            core_models.GlobalSettings.objects.create(name_app="App name")

        url = reverse("management:system_change_app_name")
        post_data = {"appName": app_name}
        response = inertia_client.post(
            url, data=post_data, content_type="application/json"
        )

        assert response.status_code == 302
        assert response.url == reverse("management:global_settings_general")

        # Request to other view to see the share props
        response = inertia_client.get(response.url)
        assert response.status_code == 200

        data = response.json()

        if create_global_settings:
            global_settings = core_models.GlobalSettings.objects.first()
            assert global_settings is not None

            if app_name:
                assert data["props"]["flash"]["success"] == "Successful name change"
                assert global_settings.name_app == app_name
            else:
                assert data["props"]["flash"]["error"] == "Exists errors on form"
                assert global_settings.name_app == "App name"
        else:
            assert data["props"]["flash"]["error"]
            assert data["props"]["errors"] == "There is not a register of settings"

    @pytest.mark.django_db
    def test_client(self, auto_login_user):
        """Client user should not have permission to access the view."""
        inertia_client, user = auto_login_user()
        assert not user.has_perm("core.can_management_global_settings")

        core_models.GlobalSettings.objects.create(name_app="App name")

        url = reverse("management:system_change_app_name")
        post_data = {"appName": "New app name"}
        response = inertia_client.post(
            url, data=post_data, content_type="application/json"
        )

        # Inertia client somehow tries to request a GET view (probably 403_error)
        assert response.status_code == 405

        global_settings = core_models.GlobalSettings.objects.first()
        assert global_settings is not None
        assert global_settings.name_app == "App name"

    @pytest.mark.django_db
    @pytest.mark.parametrize("grant_permission", [False, True])
    def test_custom(
        self,
        auto_login_custom_user,
        grant_permissions_custom_group,
        grant_permission: bool,
    ):
        """
        Custom users should only be able to access the view if their group
        has the required permission.
        """
        inertia_client, user = auto_login_custom_user()

        if grant_permission:
            grant_permissions_custom_group("can_management_global_settings")
            assert user.has_perm("core.can_management_global_settings")
        else:
            assert not user.has_perm("core.can_management_global_settings")

        core_models.GlobalSettings.objects.create(name_app="App name")

        url = reverse("management:system_change_app_name")
        post_data = {"appName": "New app name"}
        response = inertia_client.post(
            url, data=post_data, content_type="application/json"
        )

        global_settings = core_models.GlobalSettings.objects.first()
        assert global_settings is not None

        if grant_permission:
            assert response.status_code == 302
            assert response.url == reverse("management:global_settings_general")

            # Request to other view to see the share props
            response = inertia_client.get(response.url)
            assert response.status_code == 200

            data = response.json()
            assert data["props"]["flash"]["success"] == "Successful name change"

            assert global_settings.name_app == post_data["appName"]
        else:
            # Inertia client somehow tries to request a GET view (probably 403_error)
            assert response.status_code == 405

            assert global_settings.name_app == "App name"

    @pytest.mark.django_db
    def test_not_authenticated(self, inertia_client):
        """The response should redirect to the login URL."""
        url = reverse("management:system_change_app_name")
        post_data = {"appName": "New app name"}
        response = inertia_client.post(
            url, data=post_data, content_type="application/json"
        )

        assert response.status_code == 302
        assert response.url == "/login"


class TestSystemChangeSessionExpireTime:
    """Tests for the `system_change_session_expire_time` view."""

    @pytest.mark.django_db
    @pytest.mark.parametrize(
        ["create_global_settings", "session_expire_time"],
        list(product([False, True], ["", 0, 120])),
    )
    def test_manager(
        self,
        auto_login_manager_user,
        create_global_settings: bool,
        session_expire_time: Union[str, int],
    ):
        """
        The response should change session expire time and return redirect to
        global_settings_security.
        """
        inertia_client, user = auto_login_manager_user()
        assert user.has_perm("core.can_management_global_settings")

        assert not core_models.GlobalSettings.objects.exists()
        if create_global_settings:
            global_settings = core_models.GlobalSettings.objects.create()
            assert global_settings.session_expire_time == 60

        url = reverse("management:system_change_session_expire_time")
        post_data = {"sessionExpireTime": session_expire_time}
        response = inertia_client.post(
            url, data=post_data, content_type="application/json"
        )

        assert response.status_code == 302
        assert response.url == reverse("management:global_settings_security")

        # Request to other view to see the share props
        response = inertia_client.get(response.url)
        assert response.status_code == 200

        data = response.json()

        if create_global_settings:
            global_settings = core_models.GlobalSettings.objects.first()
            assert global_settings is not None

            if isinstance(session_expire_time, int):
                assert (
                    data["props"]["flash"]["success"]
                    == "Successful session expiration time change"
                )
                assert global_settings.session_expire_time == session_expire_time
            else:
                assert data["props"]["flash"]["error"] == "Exists errors on form"
                assert global_settings.session_expire_time == 60
        else:
            assert data["props"]["flash"]["error"]
            assert data["props"]["errors"] == "There is not a register of settings"

    @pytest.mark.django_db
    def test_client(self, auto_login_user):
        """Client user should not have permission to access the view."""
        inertia_client, user = auto_login_user()
        assert not user.has_perm("core.can_management_global_settings")

        global_settings = core_models.GlobalSettings.objects.create()
        assert global_settings.session_expire_time == 60

        url = reverse("management:system_change_session_expire_time")
        post_data = {"sessionExpireTime": 120}
        response = inertia_client.post(
            url, data=post_data, content_type="application/json"
        )

        # Inertia client somehow tries to request a GET view (probably 403_error)
        assert response.status_code == 405

        global_settings = core_models.GlobalSettings.objects.first()
        assert global_settings is not None
        assert global_settings.session_expire_time == 60

    @pytest.mark.django_db
    @pytest.mark.parametrize("grant_permission", [False, True])
    def test_custom(
        self,
        auto_login_custom_user,
        grant_permissions_custom_group,
        grant_permission: bool,
    ):
        """
        Custom users should only be able to access the view if their group
        has the required permission.
        """
        inertia_client, user = auto_login_custom_user()

        if grant_permission:
            grant_permissions_custom_group("can_management_global_settings")
            assert user.has_perm("core.can_management_global_settings")
        else:
            assert not user.has_perm("core.can_management_global_settings")

        global_settings = core_models.GlobalSettings.objects.create()
        assert global_settings.session_expire_time == 60

        url = reverse("management:system_change_session_expire_time")
        post_data = {"sessionExpireTime": 120}
        response = inertia_client.post(
            url, data=post_data, content_type="application/json"
        )

        global_settings = core_models.GlobalSettings.objects.first()
        assert global_settings is not None

        if grant_permission:
            assert response.status_code == 302
            assert response.url == reverse("management:global_settings_security")

            # Request to other view to see the share props
            response = inertia_client.get(response.url)
            assert response.status_code == 200

            data = response.json()
            assert (
                data["props"]["flash"]["success"]
                == "Successful session expiration time change"
            )

            assert global_settings.session_expire_time == post_data["sessionExpireTime"]
        else:
            # Inertia client somehow tries to request a GET view (probably 403_error)
            assert response.status_code == 405

            assert global_settings.session_expire_time == 60

    @pytest.mark.django_db
    def test_not_authenticated(self, inertia_client):
        """The response should redirect to the login URL."""
        url = reverse("management:system_change_session_expire_time")
        post_data = {"sessionExpireTime": 120}
        response = inertia_client.post(
            url, data=post_data, content_type="application/json"
        )

        assert response.status_code == 302
        assert response.url == "/login"


class TestSystemAppLogoChange:
    """Tests for the `system_change_app_logo` view."""

    @pytest.mark.django_db
    @pytest.mark.parametrize("create_global_settings", [False, True])
    def test_manager(
        self, auto_login_manager_user, test_image_file, create_global_settings: bool
    ):
        """
        The response should change the app logo and return redirect to
        global_settings_general.
        """
        inertia_client, user = auto_login_manager_user()
        assert user.has_perm("core.can_management_global_settings")

        assert not core_models.GlobalSettings.objects.exists()
        if create_global_settings:
            global_settings = core_models.GlobalSettings.objects.create()
            assert not global_settings.logo_app

        url = reverse("management:system_change_app_logo")
        post_data = {"logo": test_image_file}
        response = inertia_client.post(
            url, data=post_data, content_type=MULTIPART_CONTENT
        )

        assert response.status_code == 302
        assert response.url == reverse("management:global_settings_general")

        # Request to other view to see the share props
        response = inertia_client.get(response.url)
        assert response.status_code == 200

        data = response.json()

        # Created after accessing global_settings_general if it didn't exist already
        global_settings = core_models.GlobalSettings.objects.first()
        assert global_settings is not None

        if create_global_settings:
            assert data["props"]["flash"]["success"] == "Successful logo change"
            assert global_settings.logo_app
            assert global_settings.get_logo().startswith("data:image/png;base64,")
        else:
            assert data["props"]["flash"]["error"]
            assert data["props"]["errors"] == "There is not a register of settings"
            assert not global_settings.logo_app

    @pytest.mark.django_db
    @pytest.mark.parametrize("mode", ["invalid_file", "no_data"])
    def test_manager_invalid(self, auto_login_manager_user, mode: str):
        """
        The response should show error and return redirect to
        global_settings_general.
        """
        inertia_client, user = auto_login_manager_user()
        assert user.has_perm("core.can_management_global_settings")

        global_settings = core_models.GlobalSettings.objects.create()
        assert not global_settings.logo_app

        url = reverse("management:system_change_app_logo")
        if mode == "invalid_file":
            post_data = {
                "logo": ("photo.jpg", io.BytesIO(b"some random data"), "image/jpg")
            }
        else:
            post_data = {}
        response = inertia_client.post(
            url, data=post_data, content_type=MULTIPART_CONTENT
        )

        assert response.status_code == 302
        assert response.url == reverse("management:global_settings_general")

        # Request to other view to see the share props
        response = inertia_client.get(response.url)
        assert response.status_code == 200

        data = response.json()

        # Created after accessing global_settings_general if it didn't exist already
        global_settings = core_models.GlobalSettings.objects.first()
        assert global_settings is not None
        assert not global_settings.logo_app

        assert data["props"]["flash"]["error"] == "Exists errors on form"
        assert data["props"]["errors"]

        if mode == "invalid_file":
            assert data["props"]["errors"]["logo"] == [
                "Invalid file type, please choose another one."
            ]
        else:
            assert data["props"]["errors"]["logo"] == ["This field is required."]

    @pytest.mark.django_db
    def test_client(self, auto_login_user, test_image_file):
        """Client user should not have permission to access the view."""
        inertia_client, user = auto_login_user()
        assert not user.has_perm("core.can_management_global_settings")

        global_settings = core_models.GlobalSettings.objects.create()
        assert not global_settings.logo_app

        url = reverse("management:system_change_app_logo")
        post_data = {"logo": test_image_file}
        response = inertia_client.post(
            url, data=post_data, content_type=MULTIPART_CONTENT
        )

        # Inertia client somehow tries to request a GET view (probably 403_error)
        assert response.status_code == 405

        global_settings = core_models.GlobalSettings.objects.first()
        assert global_settings is not None
        assert not global_settings.logo_app

    @pytest.mark.django_db
    @pytest.mark.parametrize("grant_permission", [False, True])
    def test_custom(
        self,
        auto_login_custom_user,
        test_image_file,
        grant_permissions_custom_group,
        grant_permission: bool,
    ):
        """
        Custom users should only be able to access the view if their group
        has the required permission.
        """
        inertia_client, user = auto_login_custom_user()

        if grant_permission:
            grant_permissions_custom_group("can_management_global_settings")
            assert user.has_perm("core.can_management_global_settings")
        else:
            assert not user.has_perm("core.can_management_global_settings")

        global_settings = core_models.GlobalSettings.objects.create()
        assert not global_settings.logo_app

        url = reverse("management:system_change_app_logo")
        post_data = {"logo": test_image_file}
        response = inertia_client.post(
            url, data=post_data, content_type=MULTIPART_CONTENT
        )

        global_settings = core_models.GlobalSettings.objects.first()
        assert global_settings is not None

        if grant_permission:
            assert response.status_code == 302
            assert response.url == reverse("management:global_settings_general")

            # Request to other view to see the share props
            response = inertia_client.get(response.url)
            assert response.status_code == 200

            data = response.json()
            assert data["props"]["flash"]["success"] == "Successful logo change"

            assert global_settings.logo_app
            assert global_settings.get_logo().startswith("data:image/png;base64,")
        else:
            # Inertia client somehow tries to request a GET view (probably 403_error)
            assert response.status_code == 405

            assert not global_settings.logo_app

    @pytest.mark.django_db
    def test_not_authenticated(self, inertia_client, test_image_file):
        """The response should redirect to the login URL."""
        url = reverse("management:system_change_app_logo")
        post_data = {"logo": test_image_file}
        response = inertia_client.post(
            url, data=post_data, content_type=MULTIPART_CONTENT
        )

        assert response.status_code == 302
        assert response.url == "/login"


class TestSystemAppLogoRemove:
    """Tests for the `system_remove_app_logo` view."""

    @pytest.mark.django_db
    @pytest.mark.parametrize("create_global_settings", [False, True])
    def test_manager(
        self, auto_login_manager_user, test_image_file, create_global_settings: bool
    ):
        """
        The response should remove the app logo and return redirect to
        global_settings_general.
        """
        inertia_client, user = auto_login_manager_user()
        assert user.has_perm("core.can_management_global_settings")

        assert not core_models.GlobalSettings.objects.exists()
        if create_global_settings:
            global_settings = core_models.GlobalSettings.objects.create(
                logo_app=test_image_file
            )
            assert global_settings.logo_app
            assert global_settings.get_logo().startswith("data:image/png;base64,")

        url = reverse("management:system_remove_app_logo")
        response = inertia_client.get(url)

        assert response.status_code == 302
        assert response.url == reverse("management:global_settings_general")

        # Request to other view to see the share props
        response = inertia_client.get(response.url)
        assert response.status_code == 200

        data = response.json()

        # Created after accessing global_settings_general if it didn't exist already
        global_settings = core_models.GlobalSettings.objects.first()
        assert global_settings is not None

        if create_global_settings:
            assert data["props"]["flash"]["success"] == "Logo successfully removed"
            assert not global_settings.logo_app
        else:
            assert data["props"]["flash"]["error"]
            assert data["props"]["errors"] == "There is not a register of settings"

    @pytest.mark.django_db
    def test_client(self, auto_login_user, test_image_file):
        """Client user should not have permission to access the view."""
        inertia_client, user = auto_login_user()
        assert not user.has_perm("core.can_management_global_settings")

        global_settings = core_models.GlobalSettings.objects.create(
            logo_app=test_image_file
        )
        assert global_settings.logo_app
        assert global_settings.get_logo().startswith("data:image/png;base64,")

        url = reverse("management:system_remove_app_logo")
        response = inertia_client.get(url)

        assert response.status_code == 200

        data = response.json()
        assert data["component"] == "403Error"

        global_settings = core_models.GlobalSettings.objects.first()
        assert global_settings is not None
        assert global_settings.logo_app

    @pytest.mark.django_db
    @pytest.mark.parametrize("grant_permission", [False, True])
    def test_custom(
        self,
        auto_login_custom_user,
        test_image_file,
        grant_permissions_custom_group,
        grant_permission: bool,
    ):
        """
        Custom users should only be able to access the view if their group
        has the required permission.
        """
        inertia_client, user = auto_login_custom_user()

        if grant_permission:
            grant_permissions_custom_group("can_management_global_settings")
            assert user.has_perm("core.can_management_global_settings")
        else:
            assert not user.has_perm("core.can_management_global_settings")

        global_settings = core_models.GlobalSettings.objects.create(
            logo_app=test_image_file
        )
        assert global_settings.logo_app
        assert global_settings.get_logo().startswith("data:image/png;base64,")

        url = reverse("management:system_remove_app_logo")
        response = inertia_client.get(url)

        global_settings = core_models.GlobalSettings.objects.first()
        assert global_settings is not None

        if grant_permission:
            assert response.status_code == 302
            assert response.url == reverse("management:global_settings_general")

            # Request to other view to see the share props
            response = inertia_client.get(response.url)
            assert response.status_code == 200

            data = response.json()
            assert data["props"]["flash"]["success"] == "Logo successfully removed"

            assert not global_settings.logo_app
        else:
            assert response.status_code == 200

            data = response.json()
            assert data["component"] == "403Error"

            assert global_settings.logo_app

    @pytest.mark.django_db
    def test_not_authenticated(self, inertia_client):
        """The response should redirect to the login URL."""
        url = reverse("management:system_remove_app_logo")
        response = inertia_client.get(url)

        assert response.status_code == 302
        assert response.url == "/login"


class TestSystemActiveRegistration:
    """Tests for the `system_active_registration` view."""

    @pytest.mark.django_db
    @pytest.mark.parametrize("initial_value", [None, False, True])
    def test_manager(self, auto_login_manager_user, initial_value: Optional[bool]):
        """
        The response should enable/disable registration and return redirect to
        global_settings_general.
        """
        inertia_client, user = auto_login_manager_user()
        assert user.has_perm("core.can_management_global_settings")

        if initial_value is not None:
            core_models.GlobalSettings.objects.create(active_registration=initial_value)
        else:
            assert not core_models.GlobalSettings.objects.exists()

        url = reverse("management:system_active_registration")
        response = inertia_client.get(url)

        assert response.status_code == 302
        assert response.url == reverse("management:global_settings_general")

        # Request to other view to see the share props
        response = inertia_client.get(response.url)
        assert response.status_code == 200

        data = response.json()

        if initial_value is not None:
            success_msg = data["props"]["flash"]["success"]
            if initial_value is False:
                assert success_msg == "User registration active"
            else:
                # TODO: Fix message
                assert success_msg == "User registration deactive"

            global_settings = core_models.GlobalSettings.objects.first()
            assert global_settings is not None
            assert global_settings.active_registration != initial_value
        else:
            assert data["props"]["flash"]["error"]
            assert data["props"]["errors"] == "There is not a register of settings"

    @pytest.mark.django_db
    def test_client(self, auto_login_user):
        """Client user should not have permission to access the view."""
        inertia_client, user = auto_login_user()
        assert not user.has_perm("core.can_management_global_settings")

        url = reverse("management:system_active_registration")
        response = inertia_client.get(url)
        assert response.status_code == 200

        data = response.json()

        assert data["component"] == "403Error"

    @pytest.mark.django_db
    @pytest.mark.parametrize("grant_permission", [False, True])
    def test_custom(
        self,
        auto_login_custom_user,
        grant_permissions_custom_group,
        grant_permission: bool,
    ):
        """
        Custom users should only be able to access the view if their group
        has the required permission.
        """
        inertia_client, user = auto_login_custom_user()

        if grant_permission:
            grant_permissions_custom_group("can_management_global_settings")
            assert user.has_perm("core.can_management_global_settings")
        else:
            assert not user.has_perm("core.can_management_global_settings")

        global_settings = core_models.GlobalSettings.objects.create()
        assert global_settings.active_registration

        url = reverse("management:system_active_registration")
        response = inertia_client.get(url)

        global_settings = core_models.GlobalSettings.objects.first()
        assert global_settings is not None

        if grant_permission:
            assert response.status_code == 302
            assert response.url == reverse("management:global_settings_general")

            # Request to other view to see the share props
            response = inertia_client.get(response.url)
            assert response.status_code == 200

            data = response.json()

            assert data["props"]["flash"]["success"] == "User registration deactive"

            assert not global_settings.active_registration
        else:
            assert response.status_code == 200

            data = response.json()
            assert data["component"] == "403Error"

            assert global_settings.active_registration

    @pytest.mark.django_db
    def test_not_authenticated(self, inertia_client):
        """The response should redirect to the login URL."""
        url = reverse("management:system_active_registration")
        response = inertia_client.get(url)

        assert response.status_code == 302
        assert response.url == "/login"
