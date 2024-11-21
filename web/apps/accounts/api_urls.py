from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .apis import CheckInManagerViewSet, GateManagerViewSet, GetGroupView

router = DefaultRouter()

router.register(r'checkinmanagers', CheckInManagerViewSet,
                basename='checkinmanager')
router.register(r'gatemanagers', GateManagerViewSet,
                basename='gatemanager')

urlpatterns = [
    path("get_group/", GetGroupView.as_view(), name="get_group"),
    path('', include(router.urls)),
    path('', include('dj_rest_auth.urls')),
    path(
        'registration/', include('dj_rest_auth.registration.urls')
    ),
]
