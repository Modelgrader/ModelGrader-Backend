# from ..utility import JSONParser, JSONParserOne, passwordEncryption
from rest_framework.response import Response
from rest_framework.decorators import api_view
from ..constant import PUT
from rest_framework import status
from ..utility import extract_bearer_token
from ..services import problem_service

@api_view([PUT])
def upload_pdf(request, problem_id:str):
    file = request.FILES.get('file')
    token = extract_bearer_token(request)
    if not token:
        return Response({
            "status": "400",
            "message": "Token not found."
        }, status=status.HTTP_400_BAD_REQUEST)
    if not file:
        return Response({
            "status": "400",
            "message": "File not found."
        }, status=status.HTTP_400_BAD_REQUEST)
    response = problem_service.upload_pdf(problem_id, file, token)
    return Response({
        "status": response["status_code"],
        "message": response["message"] if "message" in response else response["error"],
    }, status=response["status_code"])