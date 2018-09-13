from schema import And, Optional

register_user_schema = {
    "username": And(str),
    "password": And(str),
    "email": And(str)
}

update_user_info_schema = {
    Optional("username"): And(str),
    Optional("password"): And(str),
    Optional("email"): And(str),
    Optional("picture_url"): And(str)
}
