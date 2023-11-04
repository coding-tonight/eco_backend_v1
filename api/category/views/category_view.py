import logging
from datetime import datetime

# from django.contrib.auth.models import User

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework import status

from category.models import Category
from category.serializer import CategorySerializer
from app import globalParameters


logger = logging.getLogger('django')


class CategoryApi(APIView):
    """ Retrive all the category , this class is readonly 
    """
    authentication_classes = []
    permission_classes = []

    def get(self, request, format=None):
        try:
            try:
                categories = Category.objects.filter(is_delete=False)

            except Category.DoesNotExist as exe:
                raise Exception(exe)

            seriailzer = CategorySerializer(categories, many=True)
            MSG = {
                globalParameters.MESSAGE: globalParameters.SUCCESS_MSG,
                'status': globalParameters.SUCCESS_CODE,
                'data': seriailzer.data
            }
            return Response(MSG, status=status.HTTP_200_OK)

        except Exception as exe:
            logger.error(str(exe), exc_info=True)
            return Response({globalParameters.MESSAGE: globalParameters.ERROR_MSG}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class AddCategoryApi(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, IsAdminUser]
    """ add category  class  only authenticated admin user can upload the create , add category
    """

    def post(self, request, format=None):
        try:
            # check if request.data is None or not
            if not request.data:
                return Response({globalParameters.MESSAGE: globalParameters.ERROR_MSG}, status=status.HTTP_400_BAD_REQUEST)

            # success message

            MSG = {
                globalParameters.MESSAGE: globalParameters.SUCCESS_MSG,
                'status': globalParameters.SUCCESS_CODE
            }

            # print(request.user)
            serializer = CategorySerializer(data=request.data)
            user = request.user
            # user = User.objects.get(user=request.user)
            # print(user)
            # check if input data is valid or not
            if serializer.is_valid():
                serializer.save(created_by=user,
                                created_at=datetime.now())

                return Response(MSG, status=status.HTTP_200_OK)
            #  serialiizer failed then
            return Response({globalParameters.MESSAGE: globalParameters.ERROR_MSG, 'error': serializer.errors}, status=status.HTTP_401_UNAUTHORIZED)

        except Exception as exe:
            logger.error(str(exe), exc_info=True)
            return Response({globalParameters.MESSAGE: globalParameters.ERROR_MSG}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CategoryDetail(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, IsAdminUser]
    """ update , get , delete category with reference id
    """

    def get(self, request, ref_id, format=None):
        try:
            try:
                category = Category.objects.get(reference_id=ref_id)

            except Category.DoesNotExist as exe:
                raise Exception(exe)

            serializer = CategorySerializer(category)

            MSG = {
                globalParameters.MESSAGE: globalParameters.SUCCESS_MSG,
                'status': globalParameters.SUCCESS_CODE,
                'data': serializer.data
            }
            return Response(MSG, status=status.HTTP_200_OK)

        except Exception as exe:
            logger.error(str(exe), exc_info=True)
            return Response({globalParameters.MESSAGE: globalParameters.ERROR_MSG, 'error': ''},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, request, ref_id, format=None):
        try:
            try:
                category = Category.objects.get(reference_id=ref_id)

            except Category.DoesNotExist as exe:
                raise Exception(exe)

            serializer = CategorySerializer(category, data=request.data)
            user = request.user
            # valid request data is valid nor not
            if serializer.is_valid():
                serializer.save(updated_at=datetime.now(),
                                updated_by=user)
                #  success message
                MSG = {
                    globalParameters.MESSAGE: globalParameters.SUCCESS_CODE,
                    'status': globalParameters.SUCCESS_CODE,
                    'data': serializer.data
                }
                return Response(MSG, status=status.HTTP_200_OK)

            return Response({globalParameters.MESSAGE: globalParameters.SUCCESS_MSG}, status=status.HTTP_401_UNAUTHORIZED)

        except Exception as exe:
            logger.error(str(exe), exc_info=True)
            return Response({globalParameters.MESSAGE: globalParameters.ERROR_MSG}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, ref_id, format=None):
        try:
            category = Category.objects.get(reference_id=ref_id)
            category.delete()
            return Response({globalParameters.MESSAGE: globalParameters.DELETE_MSG, 'status': globalParameters.SUCCESS_CODE},
                             status=status.HTTP_200_OK)

        except Category.DoesNotExist as exe:
            logger.error(str(exe), exc_info=True)
            return Response({globalParameters.MESSAGE: globalParameters.ERROR_MSG , 'status': globalParameters.ERROR_CODE_SERVER_SITE}, 
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
