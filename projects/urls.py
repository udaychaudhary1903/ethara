from django.urls import path
from . import views

app_name = 'projects'

app_name = 'projects'

urlpatterns = [
    # Project management (Manager and Admin)
    path('', views.ProjectListView.as_view(), name='project_list'),
    path('create/', views.ProjectCreateView.as_view(), name='project_create'),
    path('<int:pk>/', views.ProjectDetailView.as_view(), name='project_detail'),
    path('<int:pk>/update/', views.ProjectUpdateView.as_view(), name='project_update'),
    path('<int:pk>/delete/', views.ProjectDeleteView.as_view(), name='project_delete'),
    path('<int:pk>/assign-users/', views.assign_users_to_project, name='assign_users'),
]
