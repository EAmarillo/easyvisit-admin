from django.urls import path

from .views import UrbanizationManagerView

urlpatterns = [
    path('urbanization-manager', UrbanizationManagerView.as_view()),
    path('urbanization-manager/<int:id>', UrbanizationManagerView.as_view())
]
