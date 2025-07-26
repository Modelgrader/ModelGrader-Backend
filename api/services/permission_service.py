from ..models import Account, Problem,Testcase
from django.forms.models import model_to_dict

def canManageProblem(token, problem_id):
    """
    Check if user has permission to edit this problem
    Return: True/False
    """
    try:
        account = Account.objects.get(token=token)
        account = model_to_dict(account)
        problem = Problem.objects.get(problem_id=problem_id)
        problem = model_to_dict(problem)
        if account['account_id'] == problem['creator']:
            return True #Only creator can manage
    except (Account.DoesNotExist, Problem.DoesNotExist):
        return False