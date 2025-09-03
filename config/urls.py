from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from app.views import APIViewSet

router = DefaultRouter()

router.register("", APIViewSet, basename="")

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls))
]
