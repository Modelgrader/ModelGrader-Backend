from ..models import Problem, Testcase, ProblemGroupPermission
from django.utils import timezone

class ProblemRepository:
    def __init__(self):
        pass

    def getById(self, problem_id) -> Problem:
        return Problem.objects.get(problem_id=problem_id)
    
    def getTestcasesByProblem(self, problem, deprecated=False):
        return Testcase.objects.filter(problem=problem, deprecated=deprecated)
    
    def getTestcasesByProblemId(self, problem_id, deprecated=False):
        return Testcase.objects.filter(problem_id=problem_id, deprecated=deprecated)
    
    def getGroupPermissionsByProblem(self, problem):
        return ProblemGroupPermission.objects.filter(problem=problem)
    
    def saveProblem(self, problem) -> Problem:
        problem.save()
        return problem
    
    def createProblem(self, **kwargs) -> Problem:
        problem = Problem(**kwargs)
        problem.save()
        return problem
    
    def createTestcases(self, testcases):
        return Testcase.objects.bulk_create(testcases)
    
    def createTestcase(self, **kwargs) -> Testcase:
        testcase = Testcase(**kwargs)
        testcase.save()
        return testcase
    
    def updateTestcasesDeprecated(self, testcases, deprecated=True):
        for testcase in testcases:
            testcase.deprecated = deprecated
            testcase.save()
    
    def updateProblemTimestamp(self, problem):
        problem.updated_date = timezone.now()
        problem.save()
        return problem
