import logging

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny


from app import globalParameters

logger = logging.getLogger('django')


class DocsApiView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]
    _baseUrl = 'http://127.0.0.1:8001/'

    def get(self, request, format=None):
        try:
            MSG = {
                globalParameters.MESSAGE: 'Api Docs url',
                'urls': [
                    f'{self._baseUrl}/api/swagger/',
                    f'{self._baseUrl}/api/redoc/'
                ]
            }

            return Response(MSG, status=status.HTTP_200_OK)

        except Exception as exe:
            logger.error(str(exe), exc_info=True)
            return Response({globalParameters.MESSAGE: globalParameters.ERROR_MSG}, 
                            status=status.HTTP_200_OK)
