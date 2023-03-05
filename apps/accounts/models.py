import datetime

from django.db import models
from django.utils import timezone
from django.utils.crypto import get_random_string

from apps.core.models import CustomUser

from . import app_settings, manager


# Create your models here.
class EmailAddress(models.Model):

    user = models.ForeignKey(
        CustomUser,
        verbose_name="user",
        on_delete=models.CASCADE,
    )
    email = models.EmailField(
        unique=app_settings.UNIQUE_EMAIL,
        max_length=254,
        verbose_name="e-mail address",
    )
    verified = models.BooleanField(verbose_name="verified", default=False)
    primary = models.BooleanField(verbose_name="primary", default=False)

    objects = manager.EmailAddressManager()

    class Meta:
        verbose_name = "email address"
        verbose_name_plural = "email addresses"
        if not app_settings.UNIQUE_EMAIL:
            unique_together = [("user", "email")]

    def __str__(self):
        return self.email

    @classmethod
    def get_not_primary(cls, user: CustomUser):
        email_address = EmailAddress.objects.filter(user=user, primary=False)
        if not email_address:
            return ""
        else:
            if email_address.count() > 1:
                email_address = email_address.exclude(email=user.email)
        return email_address.first().email

    @classmethod
    def get_primary(cls, user: CustomUser):
        email_address = EmailAddress.objects.filter(user=user, primary=True)
        if not email_address:
            return ""
        return email_address.first().email

    @classmethod
    def get_or_create(cls, user: CustomUser, email: str = None):
        if email is None:
            email = user.email

        try:
            email_address = EmailAddress.objects.get(user=user, email=email)
        except EmailAddress.DoesNotExist:
            old_emails = EmailAddress.objects.filter(user=user, primary=False)
            for old_email in old_emails:
                old_email.delete()
        else:
            return email_address

        email_address = cls()
        email_address.user = user
        email_address.email = email
        email_address.save()
        return email_address

    def set_as_primary(self, conditional=False):
        old_primary = EmailAddress.objects.get_primary(self.user)
        if old_primary:
            if conditional:
                return False
            old_primary.delete()
        self.primary = True
        self.save()
        self.user.email = self.email
        self.user.save()
        return True

    def send_confirmation(self, request=None, signup=False, change=False):
        confirmation = EmailConfirmation.create(self)
        return confirmation


class EmailConfirmation(models.Model):

    email_address = models.ForeignKey(
        EmailAddress,
        verbose_name="e-mail address",
        on_delete=models.CASCADE,
    )
    created = models.DateTimeField(verbose_name="created", default=timezone.now)
    sent = models.DateTimeField(verbose_name="sent", null=True)
    key = models.CharField(verbose_name="key", max_length=64, unique=True)

    objects = manager.EmailConfirmationManager()

    class Meta:
        verbose_name = "email confirmation"
        verbose_name_plural = "email confirmations"

    def __str__(self):
        return "confirmation for %s" % self.email_address

    @classmethod
    def create(cls, email_address):
        key = get_random_string(64).lower()
        obj = cls()
        obj.email_address = email_address
        obj.key = key
        obj.save()

        return obj
        # return cls._default_manager.create(email_address=email_address, key=key)

    def key_expired(self):
        expiration_date = self.sent + datetime.timedelta(
            days=app_settings.EMAIL_CONFIRMATION_EXPIRE_DAYS
        )
        return expiration_date <= timezone.now()

    key_expired.boolean = True

    def confirm(self):
        if not self.key_expired() and not self.email_address.verified:
            email_address = self.email_address
            email_address.verified = True
            email_address.set_as_primary()
            email_address.save()
            return email_address

    @classmethod
    def can_send_cooldown_period(cls, email):
        cooldown_period = datetime.timedelta(
            seconds=app_settings.EMAIL_CONFIRMATION_COOLDOWN
        )

        try:
            email_address = EmailAddress.objects.get(email=email)
        except EmailAddress.DoesNotExist:
            return True

        send_email = not EmailConfirmation.objects.filter(
            sent__gt=timezone.now() - cooldown_period,
            email_address=email_address,
        ).exists()

        return send_email

    @classmethod
    def time_to_resend_email(cls, email):
        try:
            email_confirm = EmailConfirmation.objects.get(email_address__email=email)
        except EmailConfirmation.DoesNotExist:
            return 0

        time_sent = timezone.now() - email_confirm.sent
        cooldown_period = datetime.timedelta(
            seconds=app_settings.EMAIL_CONFIRMATION_COOLDOWN
        )

        return (cooldown_period - time_sent).total_seconds()

    @classmethod
    def delete_old_emails(cls, email_address):
        emails = EmailConfirmation.objects.filter(
            email_address=email_address,
        )
        for email in emails:
            email.delete()
