import logging
from datetime import datetime

from django.db import transaction

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.authentication import TokenAuthentication

from item.serializer import ProductSerializer
from app import globalParameters


logger = logging.getLogger('django')

""" admin views for item retrive , add , update , delete 
"""


class ItemAPIView(APIView):
    permission_classes = [IsAdminUser, IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get(self, request, format=None):
        pass

    #  handling add feature of the product 
    def post(self, request, format=None):
        try:
            data = request.data
            user = request.user

            serializer = ProductSerializer(data=data)
            if serializer.is_valid():
                serializer.save(created_at=datetime.now(),
                                created_by=user)

                MSG = {
                    globalParameters.MESSAGE: globalParameters.SUCCESS_MSG,
                    'status': globalParameters.SUCCESS_CODE,
                }
                return Response(MSG, status=status.HTTP_200_OK)

            return Response({globalParameters.MESSAGE: globalParameters.ERROR_MSG,
                             'status': globalParameters.ERROR_CODE_CLIENT_SITE},
                            status=status.HTTP_400_BAD_REQUEST)

        except Exception as exe:
            logger.error(str(exe), exc_info=True)
            return Response({globalParameters.MESSAGE: globalParameters.ERROR_MSG,
                             'status': globalParameters.ERROR_CODE_SERVER_SITE},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ItemDetailAPIView(APIView):
    permission_classes = [IsAdminUser, IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get(self, request, format=None):
        pass

    def put(self, request, format=None):
        pass

    def delete(self, request, format=None):
        pass
