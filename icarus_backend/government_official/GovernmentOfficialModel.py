from django.contrib.gis.db import models
from users.models import IcarusUser as User


class GovernmentOfficial(models.Model):
    user = models.OneToOneField(User, primary_key=True, on_delete=models.CASCADE)
    area = models.PolygonField(default='POLYGON EMPTY')
    # clearance

    def as_geojson(self):
        return {
            "type": "FeatureCollection",
            "features": [
                {
                    "geometry": {
                        "coordinates": self.area[0].coords,
                        "type": "Polygon"
                    }
                }
            ]
        }

    def as_dict(self):
        return {
            "user_id": self.user.id,
            "area": self.as_geojson()
        }
