from schema import And, Optional


class MissionViewSchemas:

    get_missions_schema = {
        "filters": And(list),
    }

    edit_mission_schema = {
        "mission_id": And(str),
        Optional("area"): And(dict),
        Optional("description"): And(str),
        Optional("title"): And(str)
    }