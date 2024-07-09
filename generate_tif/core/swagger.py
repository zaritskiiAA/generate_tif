from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from django.urls import path, include
from rest_framework import permissions


schema_view = get_schema_view(
    openapi.Info(
        title="TiffGenerate API",
        default_version="v1",
        description="""
        Здесь вы можете посмотреть работу API проекта TiffGenerate
        """
    ),
    url='http://127.0.0.1:8000',
    patterns=[
        path("api/", include('api.urls')),
    ],
    public=True,
    permission_classes=[permissions.AllowAny],
)
