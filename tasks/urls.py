from django.urls import path
from . import views

app_name = 'tasks'

urlpatterns = [
    # User views (My Tasks)
    path('my-tasks/', views.MyTasksView.as_view(), name='my_tasks'),
    path('<int:pk>/', views.TaskDetailView.as_view(), name='task_detail'),
    
    # Manager/Admin views (All Tasks)
    path('', views.TaskListView.as_view(), name='task_list'),
    path('create/', views.TaskCreateView.as_view(), name='task_create'),
    path('<int:pk>/update/', views.TaskUpdateView.as_view(), name='task_update'),
    path('<int:pk>/delete/', views.TaskDeleteView.as_view(), name='task_delete'),
    
    # AJAX endpoints
    path('<int:pk>/update-status/', views.update_task_status, name='update_task_status'),
    path('<int:pk>/add-comment/', views.add_task_comment, name='add_task_comment'),
]
