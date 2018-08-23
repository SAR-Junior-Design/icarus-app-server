# users/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models

class IcarusUser(AbstractUser):
    # add additional fields in here
    role = models.TextField() #operator, government_official

    def __str__(self):
        return self.email

    class Meta:
        db_table = 'auth_user'