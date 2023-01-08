from django.urls import include, path, re_path
from rest_framework import routers
from .views import *

router = routers.DefaultRouter()
router.register(r'chores', ChoreViewSet, 'chores')
router.register(r'rooms', RoomViewSet)
router.register(r'families', FamilyViewSet, 'families')
router.register(r'slaves', SlaveViewSet, 'slaves')
# router.register(r'invites', InviteViewSet, 'invites')
# router.register(r'users', UserViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('invites/create/', CreateInvite.as_view(), name='invite_create'),
    path('invites/list/', GetInvites.as_view(), name='invite_get'),
    path('drf-auth/', include('rest_framework.urls')),
    path('auth/', include('djoser.urls')),
    re_path(r'^auth/', include('djoser.urls.authtoken')),
]
