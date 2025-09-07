from ..models import Account

class AuthRepository:
    def __init__(self):
        pass

    def getByToken(self, token) -> Account:
        return Account.objects.get(token=token)