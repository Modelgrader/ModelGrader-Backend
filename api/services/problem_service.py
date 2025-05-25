# from ..utility import JSONParser, JSONParserOne, passwordEncryption
from ..models import Problem
from .auth_service import verifyToken
from .permission_service import canManageProblem

def verifyProblem(problem_id):
    try:
        problem = Problem.objects.get(problem_id=problem_id)
        if not problem:
            return False
        return True
    except Problem.DoesNotExist:
        return False

def upload_pdf(problem_id, file, token):
    if not verifyToken(token):
        return {
            "status_code": 401,
            "error_message": "Token expired or invalid."
        }
    if not verifyProblem(problem_id):
        return {
            "status_code": 404,
            "error_message": "Problem not found."
        }
    if not canManageProblem(token, problem_id):
        return {
            "status_code": 403,
            "error_message": "You do not have permission to manage this problem."
        }
    try:
        file_path = f"media/import-pdf/{problem_id}.pdf"
        with open(file_path, 'wb') as f:
            f.write(file.read())
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