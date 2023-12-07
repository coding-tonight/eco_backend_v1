import logging
from datetime import datetime

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.authentication import TokenAuthentication

from product.models import Color
from product.serializer import ColorSeriailizer
from app import globalParameters


logger = logging.getLogger('django')


class ColorApiView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    authentication_classes = [TokenAuthentication]
    """ retrice colors , add colors for admin users or for staff users
    """

    def get(self, request, format=None):
        try:
            try:
                colors = Color.objects.filter(is_delete=False)

            except Color.DoesNotExist as exe:
                raise Exception(exe)

            serializer = ColorSeriailizer(colors, many=True)

            MSG = {
                globalParameters.MESSAGE: globalParameters.SUCCESS_MSG,
                'status': globalParameters.SUCCESS_CODE,
                'data': serializer.data,
                'recevied_at': datetime.now()
            }
            return Response(MSG, status=status.HTTP_200_OK)

        except Exception as exe:
            logger.error(str(exe), exc_info=True)
            return Response({
                globalParameters.MESSAGE: globalParameters.ERROR_MSG,
                'status': globalParameters.ERROR_CODE_SERVER_SITE},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request, format=None):
        try:
            data = request.data
            user = request.user

            serializer = ColorSeriailizer(data=data)

            if serializer.is_valid():
                serializer.save(created_at=datetime.now(),
                                created_by=user)

                MSG = {
                    globalParameters.MESSAGE: globalParameters.SUCCESS_MSG,
                    'status': globalParameters.SUCCESS_CODE,
                    'data': serializer.data
                }
                return Response(MSG, status=status.HTTP_200_OK)

            return Response({
                globalParameters.MESSAGE: globalParameters.ERROR_MSG,
                'status': globalParameters.ERROR_CODE_CLIENT_SITE
            }, status=status.HTTP_403_FORBIDDEN)

        except Exception as exe:
            logger.error(str(exe), exc_info=True)
            return Response({
                globalParameters.MESSAGE: globalParameters.ERROR_MSG,
                'status': globalParameters.ERROR_CODE_SERVER_SITE,
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
