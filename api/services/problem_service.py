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
        return ServiceResult.error(
            message="Token expired or invalid.",
            errorType="unauthorized"
        )
    if not problem:
        return ServiceResult.error(
            message="Problem not found.",
            errorType="not_found"
        )
    if not canManageProblem(token, problem_id):
        return ServiceResult.error(
            message="You do not have permission to manage this problem.",
            errorType="forbidden"
        )
    if not check_pdf(file):
        return ServiceResult.error(
            message="The uploaded file is not a valid PDF or PDF file is too large.",
            errorType="bad_request"
        )
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