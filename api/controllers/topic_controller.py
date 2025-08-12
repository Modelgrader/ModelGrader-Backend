# from ..utility import JSONParser, JSONParserOne, passwordEncryption
from rest_framework.response import Response
from rest_framework.decorators import api_view
from ..constant import PUT, GET
from rest_framework import status
from ..utility import extract_bearer_token, ERROR_TYPE_TO_STATUS
from ..services import topic_service
from ..errors.common import *


@api_view([GET])
def topic_item_list(request, topic_id:str):
    token = extract_bearer_token(request)
    if not token:
        return InvalidTokenError().django()
    if request.method == GET:
        try:
            topic = topic_service.get_topic_item_list(topic_id, token)
            print("DOING", topic)
            return Response(status=status.HTTP_200_OK, data=topic)
        except Exception as e:
            print(e)
            if (isinstance(e, GraderException)):
                return Response({
                    "status": e.status,
                    "error": e.error
                }, status=e.status)
            else:
                return InternalServerError().django()
    else:
        return MethodNotAllowedError().django()