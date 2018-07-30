from django.contrib.gis.db import models
from django.contrib.gis.geos import Polygon
from django.contrib.auth.models import User

class Drone(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    drone_id = models.TextField()
    description = models.TextField()
    manufacturer = models.TextField()
    drone_type = models.CharField()
    color = models.CharField()
    created_at = models.DateTimeField()
