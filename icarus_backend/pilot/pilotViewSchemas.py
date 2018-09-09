from schema import And, Optional

register_pilot_schema = {
    "username": And(str),
    "password": And(str),
    "email": And(str),
    "faa_registration_number": And(str),
    "remote_pilot_certificate_number": And(str),
    "mobile_phone_number": And(str)
}

update_pilot_info_schema = {
    Optional("faa_registration_number"): And(str),
    Optional("remote_pilot_certificate_number"): And(str),
    Optional("mobile_phone_number"): And(str),
}