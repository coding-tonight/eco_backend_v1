import logging
from datetime import datetime

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework import status

from item.models import Color
from item.serializer import ColorSerilaizer
from app import globalParameters


logger = logging.getLogger('django')


class ColorAPIView(APIView):
    permission_classes = [IsAdminUser, IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    """ Retrive all color , add color
    """

    def get(self, request, format=None):
        try:
            try:
                colors = Color.objects.filter(is_delete=False)

            except Color.DoesNotExist as exe:
                raise Exception(exe)

            serializer = ColorSerilaizer(colors, many=True)
            MSG = {
                globalParameters.MESSAGE: globalParameters.SUCCESS_MSG,
                'status': globalParameters.SUCCESS_CODE,
                'data': serializer.data
            }

            return Response(MSG, status=status.HTTP_200_OK)

        except Exception as exe:
            logger.error(str(exe), exc_info=True)
            return Response({globalParameters.MESSAGE: globalParameters.ERROR_CODE_SERVER_SITE},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request, format=None):
        try:
            data = request.data
            user = request.user

            serializer = ColorSerilaizer(data=data)
            if serializer.is_valid():
                serializer.save(created_at=datetime.now(), 
                                created_by=user)
                
                MSG = {
                    globalParameters.MESSAGE: globalParameters.SUCCESS_MSG,
                    'status': globalParameters.SUCCESS_CODE,
                    'data': serializer.data
                }

                return Response(MSG, status=status.HTTP_200_OK)
            
            return Response({ globalParameters.MESSAGE: globalParameters.ERROR_MSG , 
                            'errors': serializer.errors}, 
                            status=status.HTTP_400_BAD_REQUEST)
        
        except Exception as exe:
            logger.error(str(exe), exc_info=True)
            return Response({ globalParameters.MESSAGE:globalParameters.ERROR_CODE_SERVER_SITE, 
                             'status': globalParameters.ERROR_CODE_SERVER_SITE}, 
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ColorDetailApiView(APIView):
    permission_classes = [IsAdminUser, IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get(self, request, ref_id, format=None):
        try:
            try:
                color = Color.objects.get(reference_id=ref_id)
            
            except Color.DoesNotExist as exe:
                raise Exception(exe)
            
            serializer = ColorSerilaizer(color)
            MSG = {
               globalParameters.MESSAGE: globalParameters.SUCCESS_MSG,
               'status': globalParameters.SUCCESS_CODE,
               'data': serializer.data,
               'recevied_at': datetime.now()
            }

            return Response(MSG, status=status.HTTP_200_OK)
        
        except Exception as exe:
            logger.error(str(exe), exc_info=True)
            return Response({ globalParameters.MESSAGE: globalParameters.ERROR_MSG, 
                             'status': globalParameters.ERROR_CODE_CLIENT_SITE}, 
                             status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

    def put(self, request, ref_id, format=None):
        try:
            try:
                color = Color.objects.get(reference_id=ref_id)
            
            except Color.DoesNotExist as exe:
                raise Exception(exe)
            
            data = request.data
            user = request.user

            serializer = ColorSerilaizer(color, data=data)
            if serializer.is_valid():
                serializer.save(created_at=datetime.now(), 
                                created_by=user)

                MSG = {
                  globalParameters.MESSAGE: globalParameters.SUCCESS_MSG,
                  'status': globalParameters.SUCCESS_CODE, 
                }
                return Response(MSG, status=status.HTTP_200_OK)
            
            return Response({ globalParameters.MESSAGE: globalParameters.ERROR_CODE_CLIENT_SITE}, 
                            status=status.HTTP_400_BAD_REQUEST)
        
        except Exception as exe:
            logger.error(str(exe), exc_info=True)
            return Response({globalParameters.MESSAGE: globalParameters.ERROR_MSG, 
                             'status': globalParameters.ERROR_CODE_SERVER_SITE}, 
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    def delete(self, request, ref_id, format=None):
        try: 
            Color.objects.get(reference_id=ref_id).delete()

            MSG = {
               globalParameters.MESSAGE: globalParameters.SUCCESS_MSG,
               'status': globalParameters.SUCCESS_CODE, 
            }
            return Response(MSG, status=status.HTTP_200_OK)


        except Color.DoesNotExist as exe:
            return Response({ globalParameters.MESSAGE: globalParameters.ERROR_MSG , 
                             'status': globalParameters.ERROR_CODE_SERVER_SITE},
                             status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        



