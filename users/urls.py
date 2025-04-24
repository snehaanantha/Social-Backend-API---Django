from django.urls import path
from .views import RegisterView, ProfileView, ListUsers

urlpatterns = [
    path('', RegisterView.as_view(), name='register'),
    path('profile/', ProfileView.as_view()),
    path('list/', ListUsers.as_view()),
]
