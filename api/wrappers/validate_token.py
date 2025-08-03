from api.utility import extract_bearer_token
from api.errors.common import InvalidTokenError

def validate_token(function):
    def wrapper(request, *args, **kwargs):
        token = extract_bearer_token(request)
        if not token:
            raise InvalidTokenError()
        return function(request, *args, **kwargs)
    return wrapper

