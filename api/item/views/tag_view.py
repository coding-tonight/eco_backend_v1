import logging
from datetime import datetime

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAdminUser, IsAuthenticated

from item.models import Tags
from item.serializer import TagsSerilaizer
from app import globalParameters


logger = logging.getLogger('django')


class TagApiView(APIView):
    permission_classes = []
    authentication_classes = []

    def get(self, request, format=None):
        try:
            try:
                tags = Tags.objects.filter(is_delete=False)

            except Tags.DoesNotExist as exe:
                raise Exception(exe)

            seriailier = TagsSerilaizer(tags, many=True)

            MSG = {
                globalParameters.MESSAGE: globalParameters.SUCCESS_MSG,
                'status': globalParameters.SUCCESS_CODE,
                'data': seriailier.data,
                'recevied_at': datetime.now()
            }
            return Response(MSG, status=status.HTTP_200_OK)

        except Exception as exe:
            logger.error(str(exe), exc_info=True)
            return Response({globalParameters.MESSAGE: globalParameters.SUCCESS_MSG,
                             'status': globalParameters.ERROR_CODE_SERVER_SITE
                             }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request, format=None):
        try:
            data = request.data
            user = request.user

            serializer = TagsSerilaizer(data=data)            
            
            if serializer.is_valid():
                serializer.save(created_at=datetime.now(),
                                created_by=user)
                
                MSG = {
                    globalParameters.MESSAGE: globalParameters.SUCCESS_MSG,
                    'status': globalParameters.SUCCESS_CODE,
                }
                return Response(MSG, status=status.HTTP_200_OK)
            
            return Response({ globalParameters.MESSAGE: globalParameters.ERROR_MSG
                             ,'status': globalParameters.ERROR_CODE_CLIENT_SITE},
                             status=status.HTTP_401_UNAUTHORIZED)
        
        except Exception as exe:
            logger.error(str(exe), exc_info=True)
            return Response({ globalParameters.MESSAGE: globalParameters.ERROR_MSG
                             ,'status': globalParameters.ERROR_CODE_SERVER_SITE},
                             status=status.HTTP_500_INTERNAL_SERVER_ERROR)
