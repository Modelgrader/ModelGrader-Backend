# from ..utility import JSONParser, JSONParserOne, passwordEncryption
from rest_framework.response import Response
from rest_framework.decorators import api_view
from api.sandbox.grader import PythonGrader
from ..constant import GET,POST,PUT,DELETE
from ..models import Account, Problem,Testcase
from rest_framework import status
from django.forms.models import model_to_dict
from ..serializers import *
from ..utility import extract_bearer_token

from ..controllers.problem.create_problem import *
from ..controllers.problem.update_problem import *
from ..controllers.problem.delete_problem import *
from ..controllers.problem.get_problem import *
from ..controllers.problem.get_all_problems import *
from ..controllers.problem.remove_bulk_problems import *
from ..controllers.problem.get_all_problems_by_account import *
from ..controllers.problem.validate_program import *
from ..controllers.problem.get_all_problem_with_best_submission import *
from ..controllers.problem.get_problem_in_topic_with_best_submission import *
from ..controllers.problem.update_group_permission_to_problem import *
from ..controllers.problem.get_problem_public import *
from ..services import problem_service


@api_view([PUT])
def upload_pdf(request, problem_id:str):
    file = request.FILES.get('file')
    token = extract_bearer_token(request)
    if not token:
        return Response(status=status.HTTP_400_BAD_REQUEST, data="No token")
    if not file:
        return Response(status=status.HTTP_400_BAD_REQUEST, data="No file")
    response = problem_service.upload_pdf(problem_id, file, token)
    return Response({
        "status": response.status_code,
    }, status=response.status_code)