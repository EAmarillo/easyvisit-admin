from django.shortcuts import get_object_or_404, get_list_or_404
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from .models import UrbanizationManager
from .serializers import UrbanizationManagersSerializer


# Create your views here.
class UrbanizationManagerView(GenericAPIView):
    serializer_class = UrbanizationManagersSerializer
    pagination_class = PageNumberPagination

    def get_queryset(self):
        return UrbanizationManager.objects.all()

    def post(self, request):
        serializer = UrbanizationManagersSerializer(data=request.data)
        if serializer.is_valid():

            email = serializer.validated_data['email']
            if UrbanizationManager.objects.filter(email=email).exists():
                return Response({
                    "status": "error",
                    "data": "The email already exists"
                }, status=status.HTTP_406_NOT_ACCEPTABLE
                )

            phone = serializer.validated_data['phone']
            if UrbanizationManager.objects.filter(phone=phone).exists():
                return Response({
                    "status": "error",
                    "data": "The phone already exists"
                }, status=status.HTTP_406_NOT_ACCEPTABLE
                )

            if serializer.save():
                return Response({
                    "status": "success",
                    "data": serializer.data
                },
                    status=status.HTTP_201_CREATED
                )
        else:
            return Response({
                "status": "error",
                "data": serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST
            )

    def get(self, request, id=None):
        if id:
            item = get_object_or_404(UrbanizationManager, id=id)
            serializer = UrbanizationManagersSerializer(item)
            return Response({
                "status": "success",
                "data": serializer.data
            }, status=status.HTTP_200_OK
            )

        items = get_list_or_404(UrbanizationManager)
        serializer = UrbanizationManagersSerializer(items, many=True)
        return self.get_paginated_response({
            "status": "success",
            "data": self.paginate_queryset(serializer.data)
        })

    def patch(self, request, id=None):
        item = get_object_or_404(UrbanizationManager, id=id)
        serializer = UrbanizationManagersSerializer(item, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "status": "success",
                "data": serializer.data
            }, status=status.HTTP_200_OK
            )
        else:
            return Response({
                "status": "error",
                "data": serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST
            )

    def delete(self, request, id=None):
        item = get_object_or_404(UrbanizationManager, id=id)
        item.delete()
        return Response(status=status.HTTP_202_ACCEPTED)

