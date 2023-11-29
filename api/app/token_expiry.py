from django.conf import settings

from rest_framework.authtoken.models import Token



def is_token_expiry(token):
    return token.created 


def token_expiry_handler(token):
    pass

