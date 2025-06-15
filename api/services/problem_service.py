# from ..utility import JSONParser, JSONParserOne, passwordEncryption
from ..models import Problem
from .auth_service import verifyToken
from .permission_service import canManageProblem
from ..utility import generate_random_string, check_pdf
from .service_result import ServiceResult

def verifyProblem(problem_id):
    try:
        problem = Problem.objects.get(problem_id=problem_id)
        if not problem:
            return False
        return True
    except Problem.DoesNotExist:
        return False
    
class InvalidTokenException(Exception):
    def __init__(self):
        self.message = "Token expired or invalid."
        self.status = 401
        super().__init__(self.message)

class ProblemNotFoundException(Exception):
    def __init__(self):
        self.message = "Problem not found."
        self.status = 404
        super().__init__(self.message)

class PermissionDeniedException(Exception):
    def __init__(self):
        self.message = "You do not have permission to manage this problem."
        self.status = 403
        super().__init__(self.message)

class InvalidFileException(Exception):
    pass

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
        raise InvalidTokenException()
    if not problem:
        raise ProblemNotFoundException()
    if not canManageProblem(token, problem_id):
        raise PermissionDeniedException()
    if not check_pdf(file):
        raise InvalidFileException()
    try:
        file_name = "_".join(problem.title.split()) + "#" + generate_random_string()
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