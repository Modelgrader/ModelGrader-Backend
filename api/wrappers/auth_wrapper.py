from api.services.auth_service import verifyToken
from api.utility import extract_bearer_token
from api.errors.common import InvalidTokenError

def validate_token(function):
    def wrapper(request, *args, **kwargs):
        token = extract_bearer_token(request)
        if not token:
            raise InvalidTokenError()
        is_verify = verifyToken(token)
        if not is_verify:
            raise InvalidTokenError()
        return function(request, token=token, *args, **kwargs)
    return wrapper