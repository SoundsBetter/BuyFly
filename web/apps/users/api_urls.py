from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import apis

router = DefaultRouter()

router.register(r'allusers', apis.UserViewSet, basename='user')
router.register(r'checkinmanagers', apis.CheckInManagerViewSet, basename='checkinmanager')
router.register(r'gatemanagers', apis.GateManagerViewSet, basename='gatemanager')

urlpatterns = [
    path('', include(router.urls)),
    path('dj-rest-auth/', include('dj_rest_auth.urls')),
    path(
        'dj-rest-auth/registration/', include('dj_rest_auth.registration.urls')
    ),
]
