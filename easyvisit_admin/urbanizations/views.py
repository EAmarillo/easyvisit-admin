from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from .models import Urbanization
from .serializers import UrbanizationSerializer


# Create your views here.
class UrbanizationView(GenericAPIView):
    serializer_class = UrbanizationSerializer
    pagination_class = PageNumberPagination

    def get_queryset(self):
        return Urbanization.objects.all()

    def post(self, request):
        serializer = UrbanizationSerializer(data=request.data)
        if serializer.is_valid():
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
                }, status=status.HTTP_406_NOT_ACCEPTABLE
                )
        else:
            return Response({
                "status": "error",
                "data": serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST
            )

    def get(self, request, id=None):
        if id:
            urbanization = get_object_or_404(Urbanization, id=id)
            serializer = UrbanizationSerializer(urbanization)
            return Response({
                "status": "success",
                "data": serializer.data
            }, status=status.HTTP_200_OK
            )

        items = Urbanization.objects.all()
        serializer = UrbanizationSerializer(items, many=True)
        return self.get_paginated_response({
            "status": "success",
            "data": self.paginate_queryset(serializer.data)
        })

    def patch(self, request, id=None):
        item = get_object_or_404(Urbanization, id=id)
        serializer = UrbanizationSerializer(item, data=request.data, partial=True)
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
        item = get_object_or_404(Urbanization, id=id)
        item.delete()
        return Response(status=status.HTTP_202_ACCEPTED)
