from django.contrib.gis.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Drone(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    id = models.TextField(primary_key=True)
    description = models.TextField()
    manufacturer = models.TextField()
    type = models.TextField()
    color = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)

    def as_dict(self):
        return {
            "id": self.id,
            "owner_id": self.owner.id,
            "description": self.description,
            "manufacturer": self.manufacturer,
            "type": self.type,
            "color": self.color,
            "created_at": self.created_at.isoformat()
        }