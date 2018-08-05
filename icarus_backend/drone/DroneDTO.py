
from .DroneModel import Drone
from django.contrib.auth.models import User

class DroneDTO:

    def __init__(self, owner:User, drone_id:str):
        self.owner = owner
        self.drone_id = drone_id
        self.description = None
        self.manufacturer = None
        self.drone_type = None
        self.color = None
        self.created_at = None

    def to_json(self):

        return_json = dict(self.__dict__)
        return_json["owner"] = self.owner.username
        return_json["created_at"] = str(self.created_at)

        return return_json

    def parse_from_json(self):

        pass


    @staticmethod
    def from_db_object_to_model(db_object:Drone):

        new_model_object = DroneDTO(db_object.owner,db_object.drone_id)
        new_model_object.description = db_object.description
        new_model_object.manufacturer = db_object.manufacturer
        new_model_object.drone_type = db_object.drone_type
        new_model_object.color = db_object.color
        new_model_object.created_at = db_object.created_at

        return new_model_object

    @staticmethod
    def from_model_to_db_object(model_object):

        new_drone_db_object = Drone(owner=model_object.owner,
              drone_id=model_object.drone_id,
              description=model_object.description,
              manufacturer=model_object.manufacturer,
              drone_type=model_object.drone_type,
              color=model_object.color,
              created_at=model_object.created_at)

        return new_drone_db_object

