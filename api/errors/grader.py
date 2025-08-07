from .common import GraderException

class CodeExecutionError(GraderException):
    def __init__(self):
        super().__init__("Error during editing. Your code may has an error/timeout!", 406)