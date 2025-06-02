from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    INSTALLER = 'installer'
    INTEGRATOR = 'integrator'
    DISTRIBUTOR = 'distributor'

    ROLE_CHOICES = [
        (INSTALLER, 'Installateur'),
        (INTEGRATOR, 'Integrateur'),
        (DISTRIBUTOR, 'Distributeur'),
    ]

    role = models.CharField(max_length=20, choices=ROLE_CHOICES)

    def __str__(self):
        return f"{self.username} ({self.role})"

class EmailOTP(models.Model):
    email = models.EmailField()
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        get_latest_by = "created_at"

    def __str__(self):
        return f"OTP for {self.email}"
