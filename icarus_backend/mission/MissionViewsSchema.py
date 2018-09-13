from schema import And, Optional

get_missions_schema = {
    "start_datetime": And(str),
    "end_datetime": And(str),
}