import logging
from datetime import datetime 

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.authentication import TokenAuthentication


logger = logging.getLogger('django')


class SizeAPIView(APIView):
    permission_classes = []
    authentication_classes = []

    def get(self, requet, format=None):
        pass