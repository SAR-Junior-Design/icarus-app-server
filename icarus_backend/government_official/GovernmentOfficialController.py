from django.utils.dateparse import parse_datetime
from django.utils import timezone
import datetime
from icarus_backend.mission.MissionModel import Mission


class GovernmentOfficialController:

    @staticmethod
    def jurisdiction_drone_flight_histogram(start_day, end_day, user):
        print(start_day, end_day)
        start_day = parse_datetime(start_day)
        end_day = parse_datetime(end_day)
        print(start_day, end_day)
        number_of_days = (end_day-start_day).days + 1
        print(number_of_days)
        histogram = []
        for index in range(0, number_of_days):
            print('hey:', index)
            starts_at = start_day + datetime.timedelta(days=index)
            ends_at = start_day + datetime.timedelta(days=index+1)
            print(starts_at)
            num_flights = Mission.objects.filter(starts_at__gt=starts_at, ends_at__lt=ends_at).count()
            histogram += [num_flights]
        return histogram
