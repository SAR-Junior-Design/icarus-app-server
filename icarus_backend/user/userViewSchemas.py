from schema import And

register_user_schema = {
    "username": And(str),
    "password": And(str),
    "email": And(str)
}