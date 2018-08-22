from django.contrib.gis.db import models
from django.utils import timezone
from users.models import IcarusUser as User
from icarus_backend.clearance.ClearanceModel import Clearance


class GovernmentOfficial(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    area = models.PolygonField(default='POLYGON EMPTY')
    # clearance

    def as_dict(self):
        return {
            "user_id": self.user.id,
            "area": self.area[0].coords,
        }


