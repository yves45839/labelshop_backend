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
