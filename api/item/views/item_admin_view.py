import logging
from datetime import datetime

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser , IsAuthenticated
from rest_framework.authentication import TokenAuthentication


logger = logging.getLogger('django')

""" admin views for item retrive , add , update , delete 
"""
class ItemAPIView(APIView):
    permission_classes = [IsAdminUser, IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get(self, request, format=None):
        pass


    def post(self, request, format=None):
        pass


class ItemDetailAPIView(APIView):
    permission_classes = [IsAdminUser, IsAuthenticated]
    authentication_classes = [TokenAuthentication]


    def get(self, request, format=None):
        pass


    def put(self , request, format=None):
        pass

    def delete(self, request, format=None):
        pass


