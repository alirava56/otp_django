from datetime import timedelta

from django.db import models
from django.utils import timezone


class OTP(models.Model):
    email = models.EmailField()

    code = models.CharField(
        max_length=6
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    is_used = models.BooleanField(
        default=False
    )

    def is_expired(self):
        expiration_time = (
            self.created_at +
            timedelta(minutes=2)
        )

        return timezone.now() > expiration_time

    def __str__(self):
        return f"{self.email} - {self.code}"