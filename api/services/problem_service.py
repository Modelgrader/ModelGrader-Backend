# from ..utility import JSONParser, JSONParserOne, passwordEncryption
from ..models import Problem
from .auth_service import verifyToken
from .permission_service import canManageProblem
from ..utility import generate_random_string, check_pdf

def verifyProblem(problem_id):
    try:
        problem = Problem.objects.get(problem_id=problem_id)
        if not problem:
            return False
        return True
    except Problem.DoesNotExist:
        return False

def upload_pdf(problem_id, file, token):
    problem = Problem.objects.get(problem_id=problem_id) if verifyProblem(problem_id) else None
    if not verifyToken(token):
        return {
            "status_code": 401,
            "error_message": "Token expired or invalid."
        }
    if not problem:
        return {
            "status_code": 404,
            "error_message": "Problem not found."
        }
    if not canManageProblem(token, problem_id):
        return {
            "status_code": 403,
            "error_message": "You do not have permission to manage this problem."
        }
    if not check_pdf(file):
        return {
            "status_code": 400,
            "error_message": "The uploaded file is not a valid PDF."
        }
    try:
        file_name = "_".join(problem.title.split()) + "#" + generate_random_string()
        file_path = f"media/import-pdf/{file_name}.pdf"
        with open(file_path, 'wb') as f:
            f.write(file.read())
        problem.pdf_url = file_name + ".pdf"
        problem.save()
    except Exception as e:
        return {
            "status_code": 500,
            "error_message": str(e)
        }
    return None
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