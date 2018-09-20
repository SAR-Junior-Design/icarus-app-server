from django.utils import timezone
import datetime
from icarus_backend.mission.MissionModel import Mission


class GovernmentOfficialController:

    @staticmethod
    def jurisdiction_drone_flight_histogram(start_day, end_day, user):
        number_of_days = (end_day-start_day).days + 1
        histogram = []
        for index in range(0, number_of_days):
            starts_at = start_day + datetime.timedelta(days=index)
            ends_at = start_day + datetime.timedelta(days=index+1)
            num_flights = Mission.objects.filter(starts_at__gt=starts_at, ends_at__lt=ends_at).count()
            histogram += [num_flights]
        return histogram
