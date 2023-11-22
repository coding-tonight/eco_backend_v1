import logging
from datetime import datetime

from rest_framework.views import APIView
from rest_framework.response import Response



logger = logging.getLogger('django')

class ItemAPIView(APIView):
    permission_classes = []
    authentication_classes = []

    def get(self, request, format=None):
        pass



class ItemDetailAPI(APIView):
    permission_classes = []
    authentication_classes = []

    def get(self, request, format=None):
        pass



