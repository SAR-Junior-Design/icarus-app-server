from schema import And

register_pilot_schema = {
    "username": And(str),
    "password": And(str),
    "email": And(str),
    "faa_registration_number": And(str),
    "remote_pilot_certificate_number": And(str),
    "mobile_phone_number": And(str)
}