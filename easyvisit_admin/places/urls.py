from django.urls import path

from .views import PlaceView

urlpatterns = [
    path('places', PlaceView.as_view()),
    path('places/<int:id>', PlaceView.as_view())
]
