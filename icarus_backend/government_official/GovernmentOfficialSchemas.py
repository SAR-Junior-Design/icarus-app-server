from schema import And


class GovernmentOfficialSchemas:

    upgrade_to_government_official = {
        "user_id": And(str),
        "area": {
            "type": And(str),
            "features": [{
                "properties": And(dict),
                "type": And(str),
                "geometry": {
                    "type": And(str),
                    "coordinates": And(list)
                }
            }]
        }
    }

    flight_histogram_schema = {
            "start_day": And(str),
            "end_day": And(str)
        }