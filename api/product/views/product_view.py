import logging
from datetime import datetime

from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework import status
from rest_framework.views import APIView

from product.models import Product
from product.serializer import ProductSeriailzier
from app import globalParameters


logger = logging.getLogger('django')


class ProductApiView(APIView):
    permission_classes = []
    authentication_classes = []

    def get(self, request, format=None):
        try:
            products = Product.objects.filter(is_delete=True)

        except Product.DoesNotExist as exe:
            raise Exception(exe)

        serializer = ProductSeriailzier(products, many=True)
        MSG = {
            globalParameters.MESSAGE: globalParameters.SUCCESS_MSG,
            'status': globalParameters.SUCCESS_CODE,
            'data': serializer.data
        }
        return Response(MSG, status=status.HTTP_200_OK)

    def put(self, request, format=None):
        pass



class ProductAdminApiView(APIView):
    permission_classes = [TokenAuthentication]
    authentication_classes = [IsAdminUser, IsAuthenticated]
    
    def get(self, request, format=None):
        pass