class ServiceResult:
    def __init__(self, success: bool, message: str = "", data: dict = None):
        self.success = success
        self.message = message
        self.errorType = None

    @classmethod
    def sucsess(cls, message: str = "", data: dict = None):
        return cls(success=True, message=message, data=data)
    
    @classmethod
    def error(cls, message: str = "", errorType: str = "UnknownError"):
        instance = cls(success=False, message=message)
        instance.errorType = errorType
        return instance