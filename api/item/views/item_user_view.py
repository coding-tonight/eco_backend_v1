import logging
from datetime import datetime

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from item.models import Product
from item.serializer import ProductSerializer
from app import globalParameters


logger = logging.getLogger('django')


class ProductAPIView(APIView):
    permission_classes = []
    authentication_classes = []

    def get(self, request, format=None):
        try:
            try:
                products = Product.objects.filter(is_delete=False)

            except Product.DoesNotExist as exe:
                raise Exception(exe)

            serializer = ProductSerializer(products, many=True)

            MSG = {
                globalParameters.MESSAGE: globalParameters.SUCCESS_MSG,
                'status': globalParameters.SUCCESS_CODE,
                'data': serializer.data,
                'recevied_at': datetime.now()
            }
            return Response(MSG, status=status.HTTP_200_OK)

        except Exception as exe:
            logger.error(str(exe), exc_info=True)
            return Response({globalParameters.MESSAGE: globalParameters.ERROR_MSG,
                             'status': globalParameters.ERROR_CODE_CLIENT_SITE},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ItemDetailAPI(APIView):
    permission_classes = []
    authentication_classes = []

    """ /api/<organization_slug>/customers/<customer_pk>/ for reference url
    """

    def get(self, request, ref_id, format=None):
        try:
            product = Product.objects.get(reference_id=ref_id)

        except:
            pass
