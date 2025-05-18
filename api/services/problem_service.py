# from ..utility import JSONParser, JSONParserOne, passwordEncryption
from rest_framework.response import Response
from rest_framework.decorators import api_view
from api.sandbox.grader import PythonGrader
from ..constant import GET,POST,PUT,DELETE
from ..models import Account, Problem,Testcase
from rest_framework import status
from django.forms.models import model_to_dict
from ..serializers import *

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
from .auth_service import verifyToken
from .permission_service import canManageProblem

def upload_pdf(problem_id, file, token):
    if not verifyToken(token):
        return Response(status=status.HTTP_401_UNAUTHORIZED)
    if not canManageProblem(token, problem_id):
        return Response(status=status.HTTP_403_FORBIDDEN)
    try:
        file_path = f"media/import-pdf/{problem_id}.pdf"
        with open(file_path, 'wb') as f:
            f.write(file.read())
    except Exception as e:
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    # Get user from Token
    # If not access return ... -> verify
    # Get problem from ID
    # Store file at media/import-pdf
    # Write Problem database -> pdfFilename

    """
    204: No content
    401: Unauthorized - No token / Token expired
    403: Forbidden - No permission (User found)
    500: Internal Server Error
    """

    return Response(status=status.HTTP_200_OK)