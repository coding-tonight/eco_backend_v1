import logging
from datetime import datetime

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework import status

from product.models import Tags
from product.serializer import TagsSerializer
from app import globalParameters

logger = logging.getLogger()


class TagsApiView(APIView):
    permission_classes = []
    authentication_classes = []

    def get(self, request, format=None):
        try:
            try:
                tags = Tags.objects.filter(is_delete=False)
            except Tags.DoesNotExist as exe:
                raise Exception(exe)

            serializer = TagsSerializer(tags, many=True)

            MSG = {
                globalParameters.MESSAGE: globalParameters.SUCCESS_MSG,
                'status': globalParameters.SUCCESS_CODE,
                'data': serializer.data
            }

            return Response(MSG, status=status.HTTP_200_OK)

        except Exception as exe:
            logger.error(str(exe), exc_info=True)
            return Response({
                globalParameters.MESSAGE: globalParameters.ERROR_MSG,
                'status': globalParameters.ERROR_CODE_SERVER_SITE
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class TagsAddApiView(APIView):
    pass


class TagsDetailApiView(APIView):
    permission_classes = [TokenAuthentication]
    authentication_classes = [IsAdminUser, IsAuthenticated]

    def get(self, request, ref_id , format=None):
        pass
    
    def put(self, request, ref_id , format=None):
        pass

    def delete(self, request, ref_id, format=None):
        pass
    