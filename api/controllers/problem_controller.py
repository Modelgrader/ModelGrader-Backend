# from ..utility import JSONParser, JSONParserOne, passwordEncryption
from rest_framework.response import Response
from rest_framework.decorators import api_view
from ..constant import PUT, GET
from rest_framework import status
from ..utility import extract_bearer_token, ERROR_TYPE_TO_STATUS
from ..services import problem_service
from ..errors.common import *

@api_view([PUT])
def upload_pdf(request, problem_id:str):
    try:
        file = request.FILES.get('file')
        token = extract_bearer_token(request)
        if not token:
            raise InvalidTokenError()
        if not file:
            raise InvalidFileError()
        problem_service.upload_pdf(problem_id, file, token)
        return Response(status=status.HTTP_204_NO_CONTENT)
    except Exception as e:
        if (isinstance(e, GraderException)):
            return Response({
                "status": e.status,
                "error": e.error
            }, status=e.status)
        else:
            raise InternalServerError()

@api_view([GET])
def get_problem_pdf(request, problem_id:str):
    """
    Get problem PDF file
    200: OK
    401: Unauthorized - No token / Token expired
    403: Forbidden - No permission
    404: Not Found - Problem not found
    500: Internal Server Error
    """
    pass

@api_view([GET])
def get_problem(request, problem_id:str):
    token = extract_bearer_token(request)
    if not token:
        return Response({
            "status": 401,
            "error": "Unauthorized."
        }, status=status.HTTP_401_UNAUTHORIZED)
    try:
        problem = problem_service.get_problem(problem_id, request, token)
        return Response(problem, status=status.HTTP_200_OK)
    except Exception as e:
        errStatus = 500
        if isinstance(e, problem_service.ProblemNotFoundException):
            errStatus = 404 
        elif isinstance(e, problem_service.PermissionDeniedException):
            errStatus = 403
        print("Error: ", e)
        return Response({
            "status": errStatus,
            "error": str(e)
        }, status=errStatus)