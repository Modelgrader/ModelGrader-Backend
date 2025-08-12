from rest_framework.response import Response
class GraderException(Exception):
    def __init__(self, error: str, status: int):
        self.error = error
        self.status = status
        super().__init__(self.error)

    def django(self):
        return Response(status=self.status, data={"status": self.status, "error": self.error})

class InvalidTokenError(GraderException):
    def __init__(self):
        super().__init__("Token expired or invalid.", 401)

class ItemNotFoundError(GraderException):
    def __init__(self):
        super().__init__("Item not found.", 404)

class PermissionDeniedError(GraderException):
    def __init__(self):
        super().__init__("You do not have permission.", 403)

class InvalidFileError(GraderException):
    def __init__(self):
        super().__init__("Invalid file.", 400)

class InternalServerError(GraderException):
    def __init__(self):
        super().__init__("Internal server error.", 500)

class MethodNotAllowedError(GraderException):
    def __init__(self):
        super().__init__("Method not allowed.", 405)