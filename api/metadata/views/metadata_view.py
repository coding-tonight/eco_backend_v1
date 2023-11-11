import logging
from datetime import datetime

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework import status

from metadata.models import MetaData
from metadata.serializer import MetaDataSerializer
from app import globalParameters

logger = logging.getLogger('django')


class MetaDataAPI(APIView):
    permission_classes = []
    authentication_classes = []
    """ Retrive Metadata 
    """

    def get(self, request, format=None):
        try:
            try:
                metaData = MetaData.objects.filter(is_delete=False)

            except MetaData.DoesNotExist as exe:
                raise Exception(exe)

            serializer = MetaDataSerializer(metaData, many=True)

            MSG = {
                globalParameters.MESSAGE: globalParameters.SUCCESS_MSG,
                'status': globalParameters.SUCCESS_CODE,
                'data': serializer.data,
                'recevied_time': datetime.now()
            }
            return Response(MSG, status=status.HTTP_200_OK)

        except Exception as exe:
            logger.error(str(exe), exc_info=True)
            return Response({globalParameters.MESSAGE: globalParameters.ERROR_MSG,
                             'status': globalParameters.ERROR_CODE_SERVER_SITE},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class MetaDataDetailAPI(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    authentication_classes = [TokenAuthentication]

    def get(self, request,  ref_id, format=None):
        try:
            try:
                metaData = MetaData.objects.get(reference_id=ref_id)

            except MetaData.DoesNotExist as exe:
                raise Exception(exe)

            serializer = MetaDataSerializer(metaData)

            MSG = {
                globalParameters.MESSAGE: globalParameters.SUCCESS_MSG,
                'status': globalParameters.SUCCESS_CODE,
                'data': serializer.data,
                'recevied_time': datetime.now()
            }
            return Response(MSG, status=status.HTTP_200_OK)

        except Exception as exe:
            logger.error(str(exe), exc_info=True)
            return Response({globalParameters.MESSAGE: globalParameters.ERROR_MSG,
                             'status': globalParameters.ERROR_CODE_SERVER_SITE},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, request, ref_id, format=None):
        try:
            try:
                metaData = MetaData.objects.get(reference_id=ref_id)

            except MetaData.DoesNotExist as exe:
                raise Exception(exe)

            data = request.data
            user = request.user
            serializer = MetaDataSerializer(metaData, data=data)
            if serializer.is_valid():
                serializer.save(created_at=datetime.now(), created_by=user)
                MSG = {
                    globalParameters.MESSAGE: globalParameters.SUCCESS_MSG,
                    'status': globalParameters.SUCCESS_CODE,
                    'data': serializer.data,
                    'recevied_time': datetime.now()
                }
                return Response(MSG, status=status.HTTP_200_OK)

            return Response({globalParameters.MESSAGE: globalParameters.SUCCESS_MSG,
                            'errors': serializer.errors},
                            status=status.HTTP_401_UNAUTHORIZED)
        
        except Exception as exe:
            logger.error(str(exe), exc_info=True)
            return Response({globalParameters.MESSAGE: globalParameters.ERROR_MSG,
                            'status':globalParameters.ERROR_CODE_SERVER_SITE },
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
