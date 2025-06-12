# from ..utility import JSONParser, JSONParserOne, passwordEncryption
from rest_framework.response import Response
from rest_framework.decorators import api_view
from ..constant import PUT
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
    response = problem_service.upload_pdf(problem_id, file, token)

    if not response:
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    status_code = ERROR_TYPE_TO_STATUS(response.errorType)

    return Response({
        "status": status_code,
        "error": response.message,
    }, status=status_code)