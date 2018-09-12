from schema import And

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