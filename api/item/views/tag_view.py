import logging
from datetime import datetime

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAdminUser, IsAuthenticated

from item.models import Tags
# from item.serializer import 
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
            

        
        except Exception as exe:
            logger.error(str(exe), exc_info=True)
            return Response()


    def post(self, request, format=None):
        pass
    
