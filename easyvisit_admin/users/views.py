import os.path
import csv
import io

from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from django.shortcuts import get_object_or_404, get_list_or_404

from .models import APIUser
from .serializers import APIUserSerializer, UploadCSVSerializer
from urbanizations.models import Urbanization
from urbanizations.serializers import UrbanizationSerializer
from places.models import Place
from places.serializers import PlaceSerializers


# Create your views here.
class UserView(GenericAPIView):
    serializer_class = APIUserSerializer
    pagination_class = PageNumberPagination

    def get_queryset(self):
        return APIUser.objects.all()

    def get(self, id=None):
        if id:
            user = get_object_or_404(APIUser, id=id)
            serializer = APIUserSerializer(user)
            return Response({
                "status": "success",
                "data": serializer.data
            }, status=status.HTTP_200_OK
            )

        items = get_list_or_404(APIUser)
        serializer = APIUserSerializer(items, many=True)
        return self.get_paginated_response({
            "status": "success",
            "data": self.paginate_queryset(serializer.data)
        })


class UploadCSVFileView(GenericAPIView):
    def post(self, request):
        uploadcsvserializer = UploadCSVSerializer(data=request.data)
        if uploadcsvserializer.is_valid():
            name_uploaded = uploadcsvserializer.validated_data['csv_file'].name
            uploaded_urbanization_name = os.path.splitext(name_uploaded)
            uploaded_urbanization_name = uploaded_urbanization_name[0].replace("_", " ")
            urbanization = Urbanization.objects.filter(name__iexact=uploaded_urbanization_name).first()
            if not urbanization:
                return Response({
                    "status": "error",
                    "data": "Urbanization not found, please check the file name and try again or contact with sales."
                }, status=status.HTTP_404_NOT_FOUND
                )

            urbanizationserializer = UrbanizationSerializer(urbanization)
            csv_file = uploadcsvserializer.validated_data['csv_file']
            csv_io = io.StringIO(csv_file.read().decode('utf-8'))
            csv_reader = csv.DictReader(csv_io)
            seen_combinations = set()
            for row in csv_reader:
                street = row["Street"]
                number = row["Number"]
                combination = (street, number)
                if combination in seen_combinations:
                    continue
                else:
                    seen_combinations.add(combination)
                    place = Place.objects.filter(
                        street__iexact=street,
                        number__iexact=number
                    ).first()
                    if place:
                        continue
                    else:
                        place_data = {
                            "street": row["Street"],
                            "number": row["Number"],
                            "neighborhood": row["Neighborhood"],
                            "city": urbanizationserializer.data["city"],
                            "state": urbanizationserializer.data["state"],
                            "country": urbanizationserializer.data["country"],
                            "zip_code": row["Zip Code"],
                            "is_active": True,
                            "urbanization": urbanizationserializer.data["id"]
                        }
                        save_place = PlaceSerializers(data=place_data)
                        if save_place.is_valid():
                            save_place.save()

            seen_combinations = set()
            csv_io.seek(0)
            csv_reader = csv.DictReader(csv_io)
            for row in csv_reader:
                user_identifier = row["Phone"]
                street = row["Street"]
                number = row["Number"]
                combination = (user_identifier, street, number)
                if combination in seen_combinations:
                    continue
                else:
                    seen_combinations.add(combination)
                    place = Place.objects.filter(
                        street__iexact=street,
                        number__iexact=number
                    ).first()
                    place_id = place.id
                    if place_id:
                        user = APIUser.objects.filter(
                            phone=user_identifier,
                            place=place_id
                        ).first()
                        if user:
                            continue
                        else:
                            roles = []
                            if row["Owner"] == "1":
                                roles.append(3)
                            if row["Admin"] == "1":
                                roles.append(2)
                            if row["User"] == "1":
                                roles.append(1)
                            user_data = {
                                "phone": row["Phone"],
                                "first_name": row["First Name"],
                                "last_name": row["Last Name"],
                                "email": row["Email"],
                                "is_active": True,
                                "place": place_id,
                                "roles": roles
                            }
                            save_user = APIUserSerializer(data=user_data)
                            if save_user.is_valid():
                                save_user.save()

            return Response({
                "status": "success",
                "data": []
            }, status=status.HTTP_200_OK
            )
        else:
            return Response({
                "status": "error",
                "data": uploadcsvserializer.errors
            }, status=status.HTTP_400_BAD_REQUEST
            )
