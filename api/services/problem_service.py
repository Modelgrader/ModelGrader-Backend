# from ..utility import JSONParser, JSONParserOne, passwordEncryption
from ..models import *
from .auth_service import verifyToken
from .permission_service import canManageProblem
from ..utility import generate_random_string, check_pdf
from .service_result import ServiceResult
from django.forms.models import model_to_dict
from ..errors.common import *

def verifyProblem(problem_id):
    try:
        problem = Problem.objects.get(problem_id=problem_id)
        if not problem:
            return False
        return True
    except Problem.DoesNotExist:
        return False

def get_problem(problem_id, request, token):
    try:
        problem = Problem.objects.get(problem_id=problem_id)
        testcases = Testcase.objects.filter(problem=problem,deprecated=False)
        domain = request.get_host()
        pdf_filename = problem.pdf_url
        problem.pdf_url = f"http://{domain}/media/import-pdf/{pdf_filename}"
        return {
            **model_to_dict(problem),
            "testcases": [model_to_dict(testcase) for testcase in testcases]
        }
    except Problem.DoesNotExist:
        raise ItemNotFoundError()
    except Exception as e:
        print("Error: ", e)
        raise e


def upload_pdf(problem_id, file, token):
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
    problem = Problem.objects.get(problem_id=problem_id) if verifyProblem(problem_id) else None
    if not verifyToken(token):
        raise InvalidTokenError()
    if not problem:
        raise ItemNotFoundError()
    if not canManageProblem(token, problem_id):
        raise PermissionDeniedError()
    if not check_pdf(file):
        raise InvalidFileError()
    try:
        file_name = "_".join(problem.title.split()) + "_" + generate_random_string()
        file_path = f"media/import-pdf/{file_name}.pdf"
        with open(file_path, 'wb') as f:
            f.write(file.read())
        problem.pdf_url = file_name + ".pdf"
        problem.save()
    except Exception as e:
        return ServiceResult.error(
            message=f"An error occurred while uploading the PDF: {str(e)}",
            errorType="internal_error"
        )
    return None

def get_problem_pdf(problem_id, token):
    """
    Get problem PDF file
    Permission: Owner or User with any permission that can view problem
    """
    pass