from django.contrib.gis.db import models
from users.models import IcarusUser as User


class GovernmentOfficial(models.Model):
    user = models.ForeignKey(User, primary_key=True, on_delete=models.CASCADE)
    area = models.PolygonField(default='POLYGON EMPTY')
    # clearance

    def as_dict(self):
        return {
            "user_id": self.user.id,
            "area": self.area[0].coords,
        }


