from datetime import datetime
import logging

from django.contrib.auth import authenticate
from django.contrib.auth.models import User
# from django.db import transaction

from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


from app.user_auth import user_validation
from app.validation import register_validation
from app import globalParameters


logger = logging.getLogger('django')


class Login(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request, format=None):
        try:
            """ check if request meta http authorization header has username or password not 
            """
            if not request.META.get('HTTP_AUTHORIZATION'):
                return Response({globalParameters.MESSAGE: globalParameters.ERROR_MSG},
                                status=status.HTTP_401_UNAUTHORIZED)
            
            # print(request.META.get('HTTP_AUTHORIZATION'))
            username, password = user_validation(request)
            # check if user is authenticate or not
            user = authenticate(username=username, password=password)

            if user:
                token, created = Token.objects.get_or_create(user=user)
                detail = User.objects.get(pk=user.pk)
                MSG = {
                    globalParameters.MESSAGE: globalParameters.LOGIN_MSG,
                    'status': globalParameters.SUCCESS_CODE,
                    'data': {
                        'user': user.username,
                        'email': detail.email,
                        'token': token.key,
                        'joined': detail.date_joined,
                        'is_active': detail.is_active
                    },
                    'recevied_time': datetime.now()
                }
                return Response(MSG, status=status.HTTP_200_OK)
            
            #  user is not valid then send http 403 status 
            return Response({globalParameters.MESSAGE: globalParameters.INVALID_MSG},
                            status=status.HTTP_401_UNAUTHORIZED)

        except Exception as exe:
            logger.error(str(exe), exc_info=True)
            return Response({globalParameters.MESSAGE: globalParameters.ERROR_MSG},
                            status=status.HTTP_401_UNAUTHORIZED)
        


class Register(APIView):
    permission_classes = []
    authentication_classes = []

    def post(self, request, format=None):
        try:
            username ,email ,password ,error_list = register_validation(request)

            if error_list:
                return Response({globalParameters.MESSAGE:globalParameters.ERROR_MSG}, 
                                status=status.HTTP_401_UNAUTHORIZED)
            
            is_active = True
            is_staff = False
            is_superuser = False
            # last_login = datetime.now()

            user = User(username=username, email=email, is_active=is_active, 
                        is_staff=is_staff, is_superuser=is_superuser)
            
            user.set_password(password)
            user.save()
            MSG  = {
                globalParameters.MESSAGE: 'You have register successfully.',
                'status': globalParameters.SUCCESS_CODE
            }
            return Response(MSG, status=status.HTTP_200_OK)
        
        except Exception as exe:
            logger.error(str(exe), exc_info=True)
            return Response({globalParameters.MESSAGE:globalParameters.ERROR_MSG},
                             status=status.HTTP_401_UNAUTHORIZED)
    






class LoginOut(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def delete(self, request,format=None):
        pass
