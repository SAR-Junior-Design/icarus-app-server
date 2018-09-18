from .MissionModel import Mission
from django.utils.dateparse import parse_datetime
from icarus_backend.assets.AssetModel import Asset
from django.contrib.gis.geos import Polygon


class MissionController:

    @staticmethod
    def get_missions(user, method, body):
        missions = Mission.objects
        if method == 'POST':
            filters = body['filters']
            for _filter in filters:
                if _filter['title'] == 'before':
                    missions = missions.filter(ends_at__lt=parse_datetime(_filter['datetime']))
                if _filter['title'] == 'after':
                    missions = missions.filter(starts_at__gt=parse_datetime(_filter['datetime']))
        if user.role == 'pilot':
            missions = missions.filter(created_by=user.id)
        missions = missions.all()
        dictionaries = []
        for mission in missions:
            mission_dict = mission.as_dict()
            mission_dict['num_drones'] = Asset.objects.filter(mission=mission).count()
            dictionaries += [mission_dict]
        return dictionaries

    @staticmethod
    def edit_mission(body):
        mission_id = body['mission_id']
        mission = Mission.objects.filter(pk=mission_id).first()
        if 'title' in body.keys():
            mission.title = body['title']
        if 'description' in body.keys():
            mission.description = body['description']
        if 'area' in body.keys():
            coordinates = body['area']['features'][0]['geometry']['coordinates']
            if coordinates[0][0] != coordinates[-1][0] or coordinates[0][1] != coordinates[-1][1]:
                coordinates += [coordinates[0]]
            area = Polygon(coordinates)
            mission.area = area
        mission.save()

