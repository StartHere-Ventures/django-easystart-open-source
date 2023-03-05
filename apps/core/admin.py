from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from . import models
from .forms import CustomUserChangeForm, CustomUserCreationForm


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = models.CustomUser
    list_display = (
        "email",
        "is_staff",
        "is_active",
    )
    list_filter = (
        "email",
        "is_staff",
        "is_active",
    )
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Personal info", {"fields": ("first_name", "last_name")}),
        (
            "Permissions",
            {
                "fields": (
                    "is_staff",
                    "is_active",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "password1", "password2", "is_staff", "is_active"),
            },
        ),
    )
    search_fields = ("email",)
    ordering = ("email",)


class UserProfileAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "language",
        "country",
    )
    search_fields = ["user__email", "user__username"]


class GlobalSettingsAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name_app",
    )


admin.site.register(models.CustomUser, CustomUserAdmin)
admin.site.register(models.UserProfile, UserProfileAdmin)
admin.site.register(models.GlobalSettings, GlobalSettingsAdmin)
