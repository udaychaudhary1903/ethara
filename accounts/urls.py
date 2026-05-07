from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'accounts'

app_name = 'accounts'

urlpatterns = [
    # Authentication
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    
    # Dashboard
    path('dashboard/', views.dashboard_view, name='dashboard'),
    
    # Profile
    path('profile/', views.profile_view, name='profile'),
    
    # Admin-only user management
    path('users/', views.UserListView.as_view(), name='user_list'),
    path('users/create/', views.UserCreateView.as_view(), name='user_create'),
    path('users/<int:pk>/update/', views.UserUpdateView.as_view(), name='user_update'),
    path('users/<int:pk>/delete/', views.UserDeleteView.as_view(), name='user_delete'),
    path('users/export/', views.export_users_csv, name='export_users'),
    
    # Reports (Admin only)
    path('reports/', views.reports_view, name='reports'),
]
