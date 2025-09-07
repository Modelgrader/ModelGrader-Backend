from rest_framework.response import Response
from rest_framework import status
from ..errors.common import GraderException

# def attach_django_error(e: Exception):
#     if (isinstance(e, GraderException)):
#             return Response({
#                 "status": e.status,
#                 "error": e.error
#             }, status=e.status)
#     else:
#         return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class ResponseError(Response):
    def __init__(self, code: int, error: str):
        if (isinstance(error, GraderException)):
            super().__init__(status=code, data={"status": code, "error": error.error})
        else:
            super().__init__(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
