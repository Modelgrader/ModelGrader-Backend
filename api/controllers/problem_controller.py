# from ..utility import JSONParser, JSONParserOne, passwordEncryption
from rest_framework.response import Response
from rest_framework.decorators import api_view
from ..constant import PUT, GET
from rest_framework import status
from ..utility import extract_bearer_token, ERROR_TYPE_TO_STATUS
from ..services import problem_service

@api_view([PUT])
def upload_pdf(request, problem_id:str):
    file = request.FILES.get('file')
    token = extract_bearer_token(request)
    if not token:
        return Response({
            "status": 401,
            "error": "Unauthorized."
        }, status=status.HTTP_401_UNAUTHORIZED)
    if not file:
        return Response({
            "status": 404,
            "error": "File not found."
        }, status=status.HTTP_404_NOT_FOUND)
    try:
        response = problem_service.upload_pdf(problem_id, file, token)
        return Response({
            "status": 204,
        }, status=status.HTTP_204_NO_CONTENT)
    except Exception as e:
        if isinstance(e, problem_service.InvalidTokenException):
            status = 401
        elif isinstance(e, problem_service.ProblemNotFoundException):
            status = 404
        elif isinstance(e, problem_service.PermissionDeniedException):
            status = 403
        elif isinstance(e, problem_service.InvalidFileException):
            status = 400
        else:
            status = 500
        return Response({
            "status": status,
            "error": str(e)
        }, status=status)

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