from django.contrib.gis.db import models
from django.contrib.gis.geos import Polygon

class Mission(models.Model):
    mission_id = models.TextField(primary_key=True)
    title = models.TextField()
    type = models.TextField()
    description = models.TextField()
    area = models.PolygonField(default = 'POLYGON EMPTY')
    created_at = models.DateTimeField()
    starts_at = models.DateTimeField()
    ends_at = models.DateTimeField()
    #clearance