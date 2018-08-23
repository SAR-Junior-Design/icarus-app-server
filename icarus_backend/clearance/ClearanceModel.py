from django.db import models
from django.utils import timezone
from users.models import IcarusUser as User


class Clearance(models.Model):
    clearance_id = models.TextField(primary_key=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    state = models.TextField()
    message = models.TextField()
    date = models.DateTimeField(default=timezone.now)