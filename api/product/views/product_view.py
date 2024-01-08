import logging
from datetime import datetime

# from django.core.serializers import serialize

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


class ProductAdminApiView(ProductApiView):
    permission_classes = [TokenAuthentication]
    authentication_classes = [IsAdminUser, IsAuthenticated]
    """ reterive , update and add view for for amdin users
    """

    def post(self, request, format=None):
        try:
            data = request.data
            user = request.user

            serializer = ProductSeriailzier(data=data)

            if serializer.is_valid():
                serializer.save(created_at=datetime.now(),
                                created_by=user)

                MSG = {
                    globalParameters.MESSAGE: globalParameters.SUCCESS_MSG,
                    'status': globalParameters.SUCCESS_CODE,
                    'data': serializer.data
                }
                return Response(MSG, status=status.HTTP_200_OK)

            return Response({globalParameters.MESSAGE: globalParameters.ERROR_MSG,
                             'status': globalParameters.ERROR_CODE_CLIENT_SITE,
                             'error': serializer.errors},
                            status=status.HTTP_401_UNAUTHORIZED)

        except Exception as exe:
            logger.error(str(exe), exc_info=True)
            return Response({globalParameters.MESSAGE: globalParameters.ERROR_MSG,
                             'status': globalParameters.ERROR_CODE_SERVER_SITE},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, request, ref_id, format=None):
        try:
            try:
                product = Product.objects.get(reference_id=ref_id)

            except Product.DoesNotExist as exe:
                raise Exception(exe)

            data = request.data
            user = request.user

            serializer = ProductSeriailzier(product, data=data)
            if serializer.is_valid():
                serializer.save(updated_at=datetime.now(),
                                updated_by=user)

                MSG = {
                    globalParameters.MESSAGE: globalParameters.SUCCESS_MSG,
                    'status': globalParameters.SUCCESS_CODE,
                }
                return Response(MSG, status=status.HTTP_200_OK)

            return Response({globalParameters.MESSAGE: globalParameters.SUCCESS_MSG,
                            'status': globalParameters.SUCCESS_CODE,
                            'errors': serializer.errors},
                            status=status.HTTP_401_UNAUTHORIZED)
        
        except Exception as exe:
            logger.error(str(exe), exc_info=True)
            # return Response()
            pass
            

