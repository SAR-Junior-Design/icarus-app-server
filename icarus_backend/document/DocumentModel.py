from django.db import models
from django.utils import timezone
from users.models import IcarusUser as User

class Document(models.Model):
    id = models.TextField(primary_key=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    type = models.TextField()
    location = models.TextField()