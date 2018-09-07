from schema import Schema, SchemaError
import json
from django.http import HttpResponse


def validate_body(body_schema):
    def real_decorator(f):
        def wrapper(*args, **kwargs):
            body = args[0].data
            try:
                schema = Schema([body_schema])
                schema.validate([body])
            except SchemaError as error:
                response_json = json.dumps({"message": str(error)})
                return HttpResponse(response_json, content_type="application/json", status=401)
            result = f(*args, **kwargs)
            return result
        return wrapper
    return real_decorator
