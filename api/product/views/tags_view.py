import logging 
from datetime import datetime

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework import status

from product.models import Tags
from product.serializer import TagsSerilaizer

logger = logging.getLogger()

class TagsApiView(APIView):
    permission_classes = []
    authentication_classes = []

    def get(self, request, format=None):
        try:
            try:
                tags = Tags.objects.filter(is_delete=False)
            except Tags.DoesNotExist as exe:
                raise exe
            
            # serializer = TagsSerializer()
            
        except Exception as exe:
            logger.error(str(exe), exc_info=True)
            pass

    def post(self, request, format=None):
        pass
