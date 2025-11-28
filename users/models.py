from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = (
        ('ADMIN', 'Admin'),
        ('AUTHOR', 'Author'),
        ('READER', 'Reader'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='READER')

    def is_author(self):
        return self.role == 'AUTHOR' or self.is_superuser
