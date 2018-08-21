from django.db import models

class Clearance(models.Model):
	clearance_id = models.TextField(primary_key=True)
	created_by = models.TextField()
	state = models.TextField()
	message = models.TextField()
	date = models.DateTimeField()