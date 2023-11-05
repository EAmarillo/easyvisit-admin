from django.urls import path

from .views import UploadCSVFileView, UserView

urlpatterns = [
    path('users', UserView.as_view()),
    path('upload-users', UploadCSVFileView.as_view()),
    path('users/<int:id>', UserView.as_view())
]
