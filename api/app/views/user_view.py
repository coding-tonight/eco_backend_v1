from datetime import datetime
from email.message import EmailMessage
import secrets
import logging
import smtplib

from django.contrib.auth import authenticate
from django.db import transaction
from django.contrib.auth.models import User
# from django.db import transaction

from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from app.models import OTP
from app.user_auth import user_validation
from app.validation import register_validation, forget_password_validation, verify_opt_validation, change_password_validation
from app import globalParameters


logger = logging.getLogger('django')


class Login(APIView):
    authentication_classes = []
    permission_classes = []
    """ Login class 
        logic for user login 
    """

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
                        'is_superuser': detail.is_superuser,
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
    """ user register class 
        register logic 
    """

    def post(self, request, format=None):
        try:
            username, email, password, first_name, last_name, error_list = register_validation(
                request)

            if error_list:
                return Response({globalParameters.MESSAGE: globalParameters.ERROR_MSG,
                                 'error': error_list},
                                status=status.HTTP_401_UNAUTHORIZED)

            is_active = True
            is_staff = False
            is_superuser = False
            # last_login = datetime.now()

            user = User(username=username, email=email, is_active=is_active,
                        first_name=first_name, last_name=last_name,
                        is_staff=is_staff, is_superuser=is_superuser)

            user.set_password(password)
            user.save()
            MSG = {
                globalParameters.MESSAGE: 'You have register successfully.',
                'status': globalParameters.SUCCESS_CODE
            }
            return Response(MSG, status=status.HTTP_200_OK)

        except Exception as exe:
            logger.error(str(exe), exc_info=True)
            return Response({globalParameters.MESSAGE: globalParameters.ERROR_MSG},
                            status=status.HTTP_401_UNAUTHORIZED)


""" forget password section
"""


class ForgetPassword(APIView):
    permission_classes = []
    authentication_classes = []

    """ Forget password class
        forget password logic here
        osjr qslx redg jwee  // google application password
    """

    def post(self, request, format=None):
        try:
            if not request.data:
                return Response({globalParameters.MESSAGE: globalParameters.ERROR_MSG}, status=status.HTTP_400_BAD_REQUEST)

            error_list, email, user = forget_password_validation(request)

            if error_list:
                return Response({globalParameters.MESSAGE: globalParameters.ERROR_MSG, 'error': error_list}, status=status.HTTP_401_UNAUTHORIZED)

            try:
                with transaction.atomic():
                    # send to otp to user email
                    server = smtplib.SMTP('smtp.gmail.com', 587)
                    server.starttls()

                    server.login('autonomoustechnepal@gmail.com',
                                 'osjrqslxredgjwee')

                    msg = EmailMessage()  # createing email dict or objects                     

                    otp = secrets.token_hex(4)  # generating otp
                    msg.set_content(f'Hi {email} your otp is {otp}')
                    msg['Subject'] = 'OTP for resetting your password'
                    msg['From'] = 'autonomoustechnepal@gmail.com'
                    msg['To'] = email
                    # send otp in the mail
                    server.send_message(msg)  # alternative sendmail()
                    server.close()

                    # store otp in the database
                    OTP.objects.create(email=email, otp=otp, user=user,
                                       created_at=datetime.now())

                    return Response({globalParameters.MESSAGE: "Otp is successfully send to your email."}, status=status.HTTP_200_OK)
                
            except Exception as exe:
                raise Exception(exe)

        except Exception as exe:
            logger.error(str(exe), exc_info=True)
            return Response({globalParameters.MESSAGE: globalParameters.ERROR_MSG}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class VerifyOTP(APIView):
    permission_classes = []
    authentication_classes = []

    def post(self, request):
        try:
            error_list, otp, user = verify_opt_validation(request)

            if error_list:
                return Response({globalParameters.MESSAGE: globalParameters.ERROR_MSG, 'error': error_list}, status=status.HTTP_401_UNAUTHORIZED)

            # create token if otp is verify
            token, created = Token.objects.get_or_create(user=user)
            db_otp = OTP.objects.get(otp=otp)
            db_otp.delete()

            return Response({globalParameters.MESSAGE: globalParameters.SUCCESS_MSG,
                             'status': globalParameters.SUCCESS_CODE,
                             'token': token.key,
                             'user_id': token.user_id
                             },
                            status=status.HTTP_200_OK)

        except Exception as exe:
            logger.error(str(exe), exc_info=True)
            return Response({globalParameters.MESSAGE: globalParameters.ERROR_MSG, 'status': globalParameters.ERROR_CODE_SERVER_SITE}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ChangePassword(APIView):
    permission_classes = []
    authentication_classes = [TokenAuthentication]
    """ change password class 
        logic for changing password of the user
    """

    def post(self, request, format=None):
        try:
            if not request.data:
                return Response({globalParameters.MESSAGE: globalParameters.ERROR_MSG}, status=status.HTTP_401_UNAUTHORIZED)

            error_list, password = change_password_validation(request)

            if error_list:
                return Response({globalParameters.MESSAGE: globalParameters.SUCCESS_MSG, 'error': error_list}, status=status.HTTP_401_UNAUTHORIZED)
            
            try:
                with transaction.atomic():
                    # get userintance with request.user.id
                    user = User.objects.get(id=request.user.id) 
                    user.set_password(password)
                    user.save()

                    server = smtplib.SMTP('smtp.gmail.com', 587)
                    server.starttls()

                    server.login('autonomoustechnepal@gmail.com',
                                    'osjrqslxredgjwee')

                    msg = EmailMessage()  # createing email dict or objects                     

                    msg.set_content(f'Hi {user.email} your password has been changed.')
                    msg['Subject'] = 'Password Changed Notification.'
                    msg['From'] = 'autonomoustechnepal@gmail.com'
                    msg['To'] = user.email
                    # send otp in the mail
                    server.send_message(msg)  # alternative sendmail()
                    server.close()


                    return Response({globalParameters.MESSAGE: 'Your password is successfully change.',
                                    'status': globalParameters.SUCCESS_CODE},
                                    status=status.HTTP_200_OK)
               
            except Exception as exe:
                raise Exception(exe)
            

        except Exception as exe:
            logger.error(str(exe), exc_info=True)
            return Response({globalParameters.MESSAGE: globalParameters.ERROR_CODE_SERVER_SITE}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class LoginOut(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def delete(self, request, format=None):
        try:
            user = request.user
            Token.objects.get(user_id=user).delete()
            
            MSG = {
                globalParameters.MESSAGE: globalParameters.LOGOUT_MSG,
                'status': globalParameters.SUCCESS_CODE
            }
            return Response(MSG, status=status.HTTP_200_OK)
        
        except Exception as exe:
            logger.error(str(exe), exc_info=True)
            return Response({ globalParameters.MESSAGE: globalParameters.ERROR_MSG } , status=status.HTTP_500_INTERNAL_SERVER_ERROR)