from django.contrib.gis.db import models
from django.utils import timezone

class Mission(models.Model):
    mission_id = models.TextField(primary_key=True)
    title = models.TextField()
    type = models.TextField()
    description = models.TextField()
    area = models.PolygonField(default='POLYGON EMPTY')
    created_at = models.DateTimeField(default=timezone.now)
    starts_at = models.DateTimeField()
    ends_at = models.DateTimeField()
    #clearance

    class Meta:
        permissions = (
            ('read_mission', 'Read mission'),
            ('write_mission', 'Write mission')
        )