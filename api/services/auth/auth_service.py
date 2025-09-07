from abc import abstractmethod
from django.forms.models import model_to_dict
from time import time
from api.repositories.auth_repo import AuthRepository
from ...models import Account
from ...errors.common import *

class AuthService:
    @abstractmethod
    def verifyToken(self, token) -> bool:
        pass
    
    @abstractmethod
    def getAccountByToken(self, token) -> Account:
        pass

class AuthServiceImpl(AuthService):

    def __init__(self):
        self.auth_repo = AuthRepository()

    def verifyToken(self, token) -> bool:
        try:
            account = self.auth_repo.getByToken(token)
            account_dict = model_to_dict(account)
            if account_dict['token_expire'] >= time():
                return True
            else:
                return False
        except Account.DoesNotExist:
            return False
    
    def getAccountByToken(self, token) -> Account:
        try:
            account = self.auth_repo.getByToken(token)
            account_dict = model_to_dict(account)
            if account_dict['token_expire'] >= time():
                return account
            else:
                return None
        except Account.DoesNotExist:
            return None

# Create service instances for backward compatibility
auth_service = AuthServiceImpl()

# Keep the original functions for backward compatibility
def verifyToken(token) -> bool:
    return auth_service.verifyToken(token)

def getAccountByToken(token) -> Account:
    return auth_service.getAccountByToken(token)