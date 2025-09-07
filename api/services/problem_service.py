from abc import abstractmethod
from ..models import *
from ..services.auth.auth_service import AuthServiceImpl
from .permission_service import PermissionServiceImpl
from ..repositories.problem_repo import ProblemRepository
from ..utility import generate_random_string, check_pdf
from .service_result import ServiceResult
from django.forms.models import model_to_dict
from ..errors.common import *
from ..errors.grader import *
from api.sandbox.grader import Grader
from ..serializers import *
from django.utils import timezone

class ProblemService:
    @abstractmethod
    def verifyProblem(self, problem_id) -> bool:
        pass
    
    @abstractmethod
    def get_problem(self, problem_id, request, token):
        pass
    
    @abstractmethod
    def upload_pdf(self, problem_id, file, token):
        pass
    
    @abstractmethod
    def get_problem_pdf(self, problem_id, token):
        pass
    
    @abstractmethod
    def create_problem(self, data, token):
        pass
    
    @abstractmethod
    def update_problem(self, data, token, problem_id):
        pass

class ProblemServiceImpl(ProblemService):
    
    def __init__(self):
        self.problem_repo = ProblemRepository()
        self.auth_service = AuthServiceImpl()
        self.permission_service = PermissionServiceImpl()
    
    def verifyProblem(self, problem_id) -> bool:
        try:
            problem = self.problem_repo.getProblemById(problem_id)
            if not problem:
                return False
            return True
        except Problem.DoesNotExist:
            return False

    def get_problem(self, problem_id, request, token):
        try:
            problem = self.problem_repo.getProblemById(problem_id)
            testcases = self.problem_repo.getTestcasesByProblem(problem, deprecated=False)
            group_permissions = self.problem_repo.getGroupPermissionsByProblem(problem)
            domain = request.get_host()
            pdf_filename = problem.pdf_url
            problem.pdf_url = f"http://{domain}/media/import-pdf/{pdf_filename}"
            return {
                **model_to_dict(problem),
                "testcases": [model_to_dict(testcase) for testcase in testcases],
                "group_permissions": [model_to_dict(group_permission) for group_permission in group_permissions],
            }
        except Problem.DoesNotExist:
            raise ItemNotFoundError()
        except Exception as e:
            print("Error: ", e)
            raise e


    def upload_pdf(self, problem_id, file, token):
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
        problem = self.problem_repo.getProblemById(problem_id) if self.verifyProblem(problem_id) else None
        if not self.auth_service.verifyToken(token):
            raise InvalidTokenError()
        if not problem:
            raise ItemNotFoundError()
        if not self.permission_service.canManageProblem(token, problem_id):
            raise PermissionDeniedError()
        if not check_pdf(file):
            raise InvalidFileError()
        try:
            file_name = "_".join(problem.title.split()) + "_" + generate_random_string()
            file_path = f"media/import-pdf/{file_name}.pdf"
            with open(file_path, 'wb') as f:
                f.write(file.read())
            problem.pdf_url = file_name + ".pdf"
            self.problem_repo.saveProblem(problem)
        except Exception as e:
            return ServiceResult.error(
                message=f"An error occurred while uploading the PDF: {str(e)}",
                errorType="internal_error"
            )
        return None

    def get_problem_pdf(self, problem_id, token):
        try:
            problem = self.problem_repo.getProblemById(problem_id)
            if not self.auth_service.verifyToken(token):
                raise InvalidTokenError()
            if not self.permission_service.canManageProblem(token, problem_id):
                raise PermissionDeniedError()
            
            file_path = f"media/import-pdf/{problem.pdf_url}"
            pdf_file = open(file_path, 'rb')
            
            if not pdf_file:
                raise ItemNotFoundError()

            return pdf_file
        except Problem.DoesNotExist:
            raise ItemNotFoundError()
        except Exception as e:
            raise e 
    
    def create_problem(self, data, token):
        try:
            account = self.auth_service.getAccountByToken(token)
            running_result = Grader[data['language']](data['solution'],data['testcases'],1,1.5).generate_output()

            problem = self.problem_repo.createProblem(
                language = data['language'],
                creator = account,
                title = data['title'],
                description = data['description'],
                solution = data['solution'],
                time_limit = data['time_limit'],
                allowed_languages = data['allowed_languages'],
                view_mode = data['view_mode'],
            )

            testcases = []
            for unit in running_result.data:
                testcases.append(
                    Testcase(
                        problem = problem,
                        input = unit.input,
                        output = unit.output,
                        runtime_status = unit.runtime_status,
                    )
                )

            problem_serialize = ProblemSerializer(problem)
            testcases_serialize = TestcaseSerializer(testcases,many=True)

            self.problem_repo.createTestcases(testcases)

            return problem_serialize, testcases_serialize
        except Exception as e:
            raise e
        
    def update_problem(self, data, token, problem_id):
        try:
            problem = self.problem_repo.getProblemById(problem_id)

            if not self.auth_service.verifyToken(token):
                raise InvalidTokenError()
            
            if not self.permission_service.canManageProblem(token, problem_id):
                raise PermissionDeniedError()
            
            testcases = self.problem_repo.getTestcasesByProblemId(problem_id, deprecated=False)
            
            problem.title = data.get("title",problem.title)
            problem.language = data.get("language",problem.language)
            problem.description = data.get("description",problem.description)
            problem.solution = data.get("solution",problem.solution)
            problem.time_limit = data.get("time_limit",problem.time_limit)  
            problem.is_private = data.get("is_private",problem.is_private)
            problem.allowed_languages = data.get("allowed_languages",problem.allowed_languages)
            problem.view_mode = data.get("view_mode", problem.view_mode)

            self.problem_repo.updateProblemTimestamp(problem)
            testcase_result = None
            if 'testcases' in data:
                running_result = Grader[data['language']](problem.solution,data['testcases'],1,1.5).generate_output()

                self.problem_repo.updateTestcasesDeprecated(testcases, deprecated=True)
                testcase_result = []
                for unit in running_result.data:
                    new_testcase = self.problem_repo.createTestcase(
                        problem = problem,
                        input = unit.input,
                        output = unit.output,
                        runtime_status = unit.runtime_status
                    )
                    testcase_result.append(new_testcase)
            
            if 'solution' in data:
                testcases = self.problem_repo.getTestcasesByProblem(problem, deprecated=False)
                program_input = [i.input for i in testcases]
                running_result = Grader[data['language']](problem.solution,program_input,1,1.5).generate_output()

                if not running_result.runnable:
                    raise CodeExecutionError()
                
            serialized_problem = ProblemSerializer(problem).data
            serialized_testcases = TestcaseSerializer(testcase_result or testcases, many=True).data

            self.problem_repo.saveProblem(problem)
            return serialized_problem, serialized_testcases
        except Problem.DoesNotExist:
            raise ItemNotFoundError()
        except Exception as e:
            raise e

# Create service instances for backward compatibility
problem_service = ProblemServiceImpl()

# Keep the original functions for backward compatibility
def verifyProblem(problem_id):
    return problem_service.verifyProblem(problem_id)

def get_problem(problem_id, request, token):
    return problem_service.get_problem(problem_id, request, token)

def upload_pdf(problem_id, file, token):
    return problem_service.upload_pdf(problem_id, file, token)

def get_problem_pdf(problem_id, token):
    return problem_service.get_problem_pdf(problem_id, token)

def create_problem(data, token):
    return problem_service.create_problem(data, token)

def update_problem(data, token, problem_id):
    return problem_service.update_problem(data, token, problem_id)
