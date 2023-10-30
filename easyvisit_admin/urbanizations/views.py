from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Urbanization
from .serializers import UrbanizationSerializer


# Create your views here.
class UrbanizationView(APIView):
    serializer_class = UrbanizationSerializer

    def post(self, request):
        serializer = UrbanizationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "status": "success",
                "data": serializer.data
            },
                status=status.HTTP_200_OK
            )
        else:
            return Response({
                "status": "error",
                "data": serializer.data
            }, status=status.HTTP_400_BAD_REQUEST
            )

    def get(self, request, id=None):
        if id:
            item = Urbanization.objects.get(id=id)
            serializer = UrbanizationSerializer(item)
            return Response({
                "status": "success",
                "data": serializer.data
            }, status=status.HTTP_200_OK
            )

        items = Urbanization.objects.all()
        serializer = UrbanizationSerializer(items, many=True)
        return Response({
            "status": "success",
            "data": serializer.data
        }, status=status.HTTP_200_OK
        )

