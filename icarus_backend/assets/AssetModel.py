from django.contrib.gis.db import models
from django.contrib.auth.models import User
from icarus_backend.drone.DroneModel import Drone
from icarus_backend.mission.MissionModel import Mission


class Asset(models.Model):
    drone = models.ForeignKey(Drone, on_delete=models.CASCADE)
    mission = models.ForeignKey(Mission, on_delete=models.CASCADE)
    operator = models.ForeignKey(User, on_delete=models.CASCADE)

    def as_dict(self):
        return {
            "drone_id": self.drone.id,
            "mission_id": self.mission.id,
            "operator_id": self.operator.id
        }

    class Meta:
        unique_together = (('drone', 'mission'),)
