from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.urls import reverse_lazy
from django.db.models import Q
from django.utils.decorators import method_decorator
from django.http import JsonResponse

from .models import Task, TaskComment
from .forms import TaskForm, TaskCommentForm, TaskStatusForm
from accounts.decorators import manager_required, ManagerRequiredMixin
from projects.models import Project

# User views (all authenticated users can view their tasks)
@method_decorator(login_required, name='dispatch')
class MyTasksView(ListView):
    model = Task
    template_name = 'tasks/my_tasks.html'
    context_object_name = 'tasks'
    paginate_by = 20
    
    def get_queryset(self):
        user = self.request.user
        queryset = Task.objects.filter(assigned_to=user)
        
        # Apply filters
        status = self.request.GET.get('status')
        priority = self.request.GET.get('priority')
        search = self.request.GET.get('search')
        
        if status:
            queryset = queryset.filter(status=status)
        
        if priority:
            queryset = queryset.filter(priority=priority)
        
        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) | Q(description__icontains=search)
            )
        
        return queryset.order_by('-created_at')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search'] = self.request.GET.get('search', '')
        context['selected_status'] = self.request.GET.get('status', '')
        context['selected_priority'] = self.request.GET.get('priority', '')
        context['status_choices'] = Task.STATUS_CHOICES
        context['priority_choices'] = Task.PRIORITY_CHOICES
        return context

@method_decorator(login_required, name='dispatch')
class TaskDetailView(DetailView):
    model = Task
    template_name = 'tasks/task_detail.html'
    context_object_name = 'task'
    
    def get_queryset(self):
        user = self.request.user
        
        if user.is_admin:
            return Task.objects.all()
        elif user.is_manager:
            # Manager can see tasks from their projects
            return Task.objects.filter(
                Q(assigned_to=user) | 
                Q(project__created_by=user) | 
                Q(project__assigned_users=user)
            ).distinct()
        else:
            # Regular user can only see their assigned tasks
            return Task.objects.filter(assigned_to=user)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        task = self.get_object()
        context['comments'] = task.comments.all().order_by('-created_at')
        context['comment_form'] = TaskCommentForm()
        context['status_form'] = TaskStatusForm(instance=task)
        return context

# Manager and Admin views
@method_decorator([login_required, manager_required], name='dispatch')
class TaskListView(ListView):
    model = Task
    template_name = 'tasks/task_list.html'
    context_object_name = 'tasks'
    paginate_by = 20
    
    def get_queryset(self):
        user = self.request.user
        
        if user.is_admin:
            queryset = Task.objects.all()
        else:
            # Manager can see tasks from their projects
            user_projects = Project.objects.filter(
                Q(created_by=user) | Q(assigned_users=user)
            ).distinct()
            queryset = Task.objects.filter(project__in=user_projects)
        
        # Apply filters
        project_id = self.request.GET.get('project')
        assigned_to = self.request.GET.get('assigned_to')
        status = self.request.GET.get('status')
        priority = self.request.GET.get('priority')
        search = self.request.GET.get('search')
        
        if project_id:
            queryset = queryset.filter(project_id=project_id)
        
        if assigned_to:
            queryset = queryset.filter(assigned_to_id=assigned_to)
        
        if status:
            queryset = queryset.filter(status=status)
        
        if priority:
            queryset = queryset.filter(priority=priority)
        
        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) | Q(description__icontains=search)
            )
        
        return queryset.order_by('-created_at')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        
        if user.is_admin:
            context['projects'] = Project.objects.all()
        else:
            context['projects'] = Project.objects.filter(
                Q(created_by=user) | Q(assigned_users=user)
            ).distinct()
        
        context['search'] = self.request.GET.get('search', '')
        context['selected_project'] = self.request.GET.get('project', '')
        context['selected_assigned_to'] = self.request.GET.get('assigned_to', '')
        context['selected_status'] = self.request.GET.get('status', '')
        context['selected_priority'] = self.request.GET.get('priority', '')
        context['status_choices'] = Task.STATUS_CHOICES
        context['priority_choices'] = Task.PRIORITY_CHOICES
        return context

@method_decorator([login_required, manager_required], name='dispatch')
class TaskCreateView(CreateView):
    model = Task
    form_class = TaskForm
    template_name = 'tasks/task_form.html'
    success_url = reverse_lazy('tasks:task_list')
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs
    
    def form_valid(self, form):
        form.instance.created_by = self.request.user
        messages.success(self.request, 'Task created successfully!')
        return super().form_valid(form)

@method_decorator([login_required, manager_required], name='dispatch')
class TaskUpdateView(UpdateView):
    model = Task
    form_class = TaskForm
    template_name = 'tasks/task_form.html'
    success_url = reverse_lazy('tasks:task_list')
    
    def get_queryset(self):
        user = self.request.user
        if user.is_admin:
            return Task.objects.all()
        else:
            # Manager can update tasks from their projects
            user_projects = Project.objects.filter(
                Q(created_by=user) | Q(assigned_users=user)
            ).distinct()
            return Task.objects.filter(project__in=user_projects)
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs
    
    def form_valid(self, form):
        messages.success(self.request, 'Task updated successfully!')
        return super().form_valid(form)

@method_decorator([login_required, manager_required], name='dispatch')
class TaskDeleteView(DeleteView):
    model = Task
    template_name = 'tasks/task_confirm_delete.html'
    success_url = reverse_lazy('tasks:task_list')
    
    def get_queryset(self):
        user = self.request.user
        if user.is_admin:
            return Task.objects.all()
        else:
            # Manager can delete tasks from their projects
            user_projects = Project.objects.filter(
                Q(created_by=user) | Q(assigned_users=user)
            ).distinct()
            return Task.objects.filter(project__in=user_projects)
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Task deleted successfully!')
        return super().delete(request, *args, **kwargs)

@login_required
def update_task_status(request, pk):
    """AJAX view to update task status"""
    task = get_object_or_404(Task, pk=pk)
    user = request.user
    
    # Check permissions
    can_update = (
        user.is_admin or 
        task.assigned_to == user or 
        (user.is_manager and (task.project.created_by == user or user in task.project.assigned_users.all()))
    )
    
    if not can_update:
        return JsonResponse({'error': 'Permission denied'}, status=403)
    
    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status in dict(Task.STATUS_CHOICES):
            task.status = new_status
            task.save()
            
            return JsonResponse({
                'success': True,
                'status': task.get_status_display(),
                'status_value': task.status
            })
        else:
            return JsonResponse({'error': 'Invalid status'}, status=400)
    
    return JsonResponse({'error': 'Method not allowed'}, status=405)

@login_required
def add_task_comment(request, pk):
    """AJAX view to add comment to task"""
    task = get_object_or_404(Task, pk=pk)
    user = request.user
    
    # Check permissions (same as task detail view)
    can_comment = (
        user.is_admin or 
        task.assigned_to == user or 
        (user.is_manager and (task.project.created_by == user or user in task.project.assigned_users.all()))
    )
    
    if not can_comment:
        return JsonResponse({'error': 'Permission denied'}, status=403)
    
    if request.method == 'POST':
        comment_text = request.POST.get('comment')
        if comment_text:
            comment = TaskComment.objects.create(
                task=task,
                user=user,
                comment=comment_text
            )
            
            return JsonResponse({
                'success': True,
                'comment': {
                    'id': comment.id,
                    'user': comment.user.get_full_name() or comment.user.username,
                    'comment': comment.comment,
                    'created_at': comment.created_at.strftime('%Y-%m-%d %H:%M')
                }
            })
        else:
            return JsonResponse({'error': 'Comment cannot be empty'}, status=400)
    
    return JsonResponse({'error': 'Method not allowed'}, status=405)
