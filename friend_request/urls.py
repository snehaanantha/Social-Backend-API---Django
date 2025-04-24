# from django.urls import path
# from .views import FriendRequestViewSet

# friend_request = FriendRequestViewSet.as_view({
#     'post': 'send'
# })
# respond = FriendRequestViewSet.as_view({
#     'post': 'respond'
# })
# suggestions = FriendRequestViewSet.as_view({
#     'get': 'suggestions'
# })
# friends = FriendRequestViewSet.as_view({
#     'get': 'friends'
# })

# urlpatterns = [
#     path('request/', friend_request),
#     path('respond/', respond),
#     path('suggestions/', suggestions),
#     path('', friends),
# ]

# urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import FriendRequestViewSet

router = DefaultRouter()
router.register(r'', FriendRequestViewSet, basename='friends')

urlpatterns = [
    path('', include(router.urls)),
]

