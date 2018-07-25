from django.db import models;

class Mission(models.Model):
    mission_id = models.TextField(primary_key=True)
    title = models.TextField()
    type = models.TextField()
    description = models.TextField()
    #area
    created_at = models.DateTimeField()
    starts_at = models.DateTimeField()
    ends_at = models.DateTimeField()
    closed_at = models.DateTimeField()
    #clearance