from .MissionModel import Mission
from django.utils.dateparse import parse_datetime
from icarus_backend.assets.AssetModel import Asset


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

