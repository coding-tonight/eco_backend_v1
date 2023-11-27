import logging
from datetime import datetime

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.authentication import TokenAuthentication

from item.models import Size
from item.serializer import SizeSerializer
from app import globalParameters


logger = logging.getLogger('django')


class SizeAPIView(APIView):
    permission_classes = [IsAdminUser, IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get(self, requet, format=None):
        try:
            try:
                sizes = Size.objects.filter(is_delete=False)

            except Size.DoesNotExist as exe:
                raise Exception(exe)

            serializer = SizeSerializer(sizes, many=True)
            MSG = {
                globalParameters.MESSAGE: globalParameters.SUCCESS_MSG,
                'status': globalParameters.SUCCESS_CODE,
                'data': serializer.data
            }
            return Response(MSG, status=status.HTTP_200_OK)

        except Exception as exe:
            logger.error(str(exe), exc_info=True)
            return Response({globalParameters.MESSAGE: globalParameters.ERROR_MSG,
                             'status': globalParameters.ERROR_CODE_SERVER_SITE},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request, format=None):
        try:
            data = request.data
            user = request.user

            serializer = SizeSerializer(data=data)
            if serializer.is_valid():
                serializer.save(created_at=datetime.now(), 
                                created_by=user)
                MSG = {
                    globalParameters.MESSAGE: globalParameters.SUCCESS_MSG,
                    'status': globalParameters.SUCCESS_CODE,
                }

                return Response(MSG, status=status.HTTP_200_OK)
            
            return Response({ globalParameters.MESSAGE: globalParameters.ERROR_MSG}, 
                            status=status.HTTP_400_BAD_REQUEST)

        except Exception as exe:
            logger.error(str(exe), exc_info=True)
            return Response({ globalParameters.MESSAGE: globalParameters.ERROR_MSG}, 
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class SizeDetailApiView(APIView):
    try:
        size = Size.objects.filter(is_delete=False)
    
    except Size.DoesNotExist as exe:
        pass
