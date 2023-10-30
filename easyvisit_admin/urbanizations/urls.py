from django.urls import path

from .views import UrbanizationView

urlpatterns = [
    path('urbanization', UrbanizationView.as_view()),
    path('urbanization/<int:id>', UrbanizationView.as_view())
]
