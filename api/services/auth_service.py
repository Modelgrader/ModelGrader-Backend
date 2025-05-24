from django.forms.models import model_to_dict
from time import time
from ..models import Account

def verifyToken(token):
    """
    Check if user has valid token and not expired
    Return: True/False
    """
    try:
        account = Account.objects.get(token=token)
        account_dict = model_to_dict(account)
        if account_dict['token_expire'] >= time():
            return True
        else:
            return False
    except Account.DoesNotExist:
        return False