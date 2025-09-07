from abc import abstractmethod
from django.forms.models import model_to_dict
from ..repositories.permission_repo import PermissionRepository
from ..models import Account, Problem

class PermissionService:
    @abstractmethod
    def canManageProblem(self, token, problem_id) -> bool:
        pass

class PermissionServiceImpl(PermissionService):
    
    def __init__(self):
        self.permission_repo = PermissionRepository()
    
    def canManageProblem(self, token, problem_id) -> bool:
        """
        Check if user has permission to edit this problem
        Return: True/False
        """
        try:
            account = self.permission_repo.getAccountByToken(token)
            account_dict = model_to_dict(account)
            problem = self.permission_repo.getProblemById(problem_id)
            problem_dict = model_to_dict(problem)
            if account_dict['account_id'] == problem_dict['creator']:
                return True  # Only creator can manage
        except (Account.DoesNotExist, Problem.DoesNotExist):
            return False
        return False

# Create service instances for backward compatibility
permission_service = PermissionServiceImpl()

# Keep the original function for backward compatibility
def canManageProblem(token, problem_id):
    return permission_service.canManageProblem(token, problem_id)