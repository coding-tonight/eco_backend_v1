import logging
from datetime import datetime

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework import status


logger = logging.getLogger('django')


class ColorAPIView(APIView):
    permission_classes = []
    authentication_classes = []

    def get(self, request, format=None):
        pass

    def post(self, request, format=None):
        pass