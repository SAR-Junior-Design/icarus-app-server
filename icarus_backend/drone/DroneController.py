from .DroneModel import Drone
from django.contrib.auth.models import User
from .DroneDTO import DroneDTO

class DroneController:


    @staticmethod
    def get_user_drones(user_object:User):
        user_drones = Drone.objects.get(user=user_object)


        dto_objects = []
        for drone_db_object in user_drones:
            drone_dto_object = DroneDTO.from_db_object_to_model(drone_db_object)
            dto_objects.append(drone_db_object)

        return dto_objects
