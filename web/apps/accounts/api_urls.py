from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import apis

router = DefaultRouter()

router.register(r'checkinmanagers', apis.CheckInManagerViewSet,
                basename='checkinmanager')
router.register(r'gatemanagers', apis.GateManagerViewSet,
                basename='gatemanager')

urlpatterns = [
    path('', include(router.urls)),
    path('', include('dj_rest_auth.urls')),
    path(
        'registration/', include('dj_rest_auth.registration.urls')
    ),
]
