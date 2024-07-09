from django.urls import path

from .views import CreateTiffFile

urlpatterns = [
    path('create_tiff/', CreateTiffFile.as_view(), name='create_tiff'),
]
