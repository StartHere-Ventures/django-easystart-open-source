from django.contrib import admin

from . import models


class EmailAddressAdmin(admin.ModelAdmin):
    list_display = ("email", "user", "primary", "verified")
    list_filter = ("primary", "verified")
    search_fields = []
    raw_id_fields = ("user",)


class EmailConfirmationAdmin(admin.ModelAdmin):
    list_display = ("email_address", "created", "sent", "key")
    list_filter = ("sent",)
    raw_id_fields = ("email_address",)


admin.site.register(models.EmailConfirmation, EmailConfirmationAdmin)
admin.site.register(models.EmailAddress, EmailAddressAdmin)
