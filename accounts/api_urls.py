from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from . import api_views

urlpatterns = [
    # JWT Authentication
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # API endpoints
    path('users/', api_views.UserListCreateAPIView.as_view(), name='user_list_create'),
    path('users/<int:pk>/', api_views.UserRetrieveUpdateDestroyAPIView.as_view(), name='user_detail'),
    path('profile/', api_views.UserProfileAPIView.as_view(), name='user_profile'),
]
