from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.db.models import Q, Count
from django.http import JsonResponse, HttpResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
import csv
import json

from .models import User, UserProfile
from .forms import UserRegistrationForm, UserUpdateForm, ProfileUpdateForm
from .decorators import admin_required, manager_required
from projects.models import Project
from tasks.models import Task

def login_view(request):
    if request.user.is_authenticated:
        return redirect('accounts:dashboard')
    
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            next_url = request.GET.get('next', 'accounts:dashboard')
            return redirect(next_url)
        else:
            messages.error(request, 'Invalid username or password.')
    
    return render(request, 'accounts/login.html')

@login_required
def dashboard_view(request):
    user = request.user
    context = {
        'user': user,
    }
    
    if user.is_admin:
        context.update({
            'total_users': User.objects.count(),
            'total_projects': Project.objects.count(),
            'total_tasks': Task.objects.count(),
            'active_projects': Project.objects.filter(status='active').count(),
            'recent_users': User.objects.order_by('-date_joined')[:5],
            'recent_projects': Project.objects.order_by('-created_at')[:5],
        })
        return render(request, 'accounts/admin_dashboard.html', context)
    
    elif user.is_manager:
        user_projects = Project.objects.filter(
            Q(created_by=user) | Q(assigned_users=user)
        ).distinct()
        context.update({
            'my_projects': user_projects,
            'total_projects': user_projects.count(),
            'team_tasks': Task.objects.filter(project__in=user_projects),
            'pending_tasks': Task.objects.filter(
                project__in=user_projects, 
                status__in=['todo', 'in_progress']
            ).count(),
        })
        return render(request, 'accounts/manager_dashboard.html', context)
    
    else:  # regular user
        my_tasks = Task.objects.filter(assigned_to=user)
        context.update({
            'my_tasks': my_tasks.order_by('-created_at')[:10],
            'total_tasks': my_tasks.count(),
            'pending_tasks': my_tasks.filter(status__in=['todo', 'in_progress']).count(),
            'completed_tasks': my_tasks.filter(status='completed').count(),
        })
        return render(request, 'accounts/user_dashboard.html', context)

@login_required
def profile_view(request):
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, request.FILES, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, instance=profile)
        
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile has been updated!')
            return redirect('accounts:profile')
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=profile)
    
    context = {
        'user_form': user_form,
        'profile_form': profile_form
    }
    return render(request, 'accounts/profile.html', context)

# Admin-only views
@method_decorator([login_required, admin_required], name='dispatch')
class UserListView(ListView):
    model = User
    template_name = 'accounts/user_list.html'
    context_object_name = 'users'
    paginate_by = 20
    
    def get_queryset(self):
        queryset = User.objects.all().order_by('-date_joined')
        search = self.request.GET.get('search')
        role = self.request.GET.get('role')
        
        if search:
            queryset = queryset.filter(
                Q(username__icontains=search) |
                Q(first_name__icontains=search) |
                Q(last_name__icontains=search) |
                Q(email__icontains=search)
            )
        
        if role:
            queryset = queryset.filter(role=role)
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search'] = self.request.GET.get('search', '')
        context['selected_role'] = self.request.GET.get('role', '')
        context['roles'] = User.ROLE_CHOICES
        return context

@method_decorator([login_required, admin_required], name='dispatch')
class UserCreateView(CreateView):
    model = User
    form_class = UserRegistrationForm
    template_name = 'accounts/user_form.html'
    success_url = reverse_lazy('accounts:user_list')
    
    def form_valid(self, form):
        messages.success(self.request, 'User created successfully!')
        return super().form_valid(form)

@method_decorator([login_required, admin_required], name='dispatch')
class UserUpdateView(UpdateView):
    model = User
    form_class = UserUpdateForm
    template_name = 'accounts/user_form.html'
    success_url = reverse_lazy('accounts:user_list')
    
    def form_valid(self, form):
        messages.success(self.request, 'User updated successfully!')
        return super().form_valid(form)

@method_decorator([login_required, admin_required], name='dispatch')
class UserDeleteView(DeleteView):
    model = User
    template_name = 'accounts/user_confirm_delete.html'
    success_url = reverse_lazy('accounts:user_list')
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, 'User deleted successfully!')
        return super().delete(request, *args, **kwargs)

@login_required
@admin_required
def export_users_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="users.csv"'
    
    writer = csv.writer(response)
    writer.writerow(['Username', 'First Name', 'Last Name', 'Email', 'Role', 'Date Joined', 'Last Login'])
    
    users = User.objects.all()
    for user in users:
        writer.writerow([
            user.username,
            user.first_name,
            user.last_name,
            user.email,
            user.get_role_display(),
            user.date_joined.strftime('%Y-%m-%d %H:%M:%S'),
            user.last_login.strftime('%Y-%m-%d %H:%M:%S') if user.last_login else 'Never'
        ])
    
    return response

@login_required
@admin_required
def reports_view(request):
    # User statistics
    user_stats = {
        'total_users': User.objects.count(),
        'admin_count': User.objects.filter(role='admin').count(),
        'manager_count': User.objects.filter(role='manager').count(),
        'user_count': User.objects.filter(role='user').count(),
        'active_users': User.objects.filter(is_active=True).count(),
    }
    
    # Project statistics
    project_stats = {
        'total_projects': Project.objects.count(),
        'active_projects': Project.objects.filter(status='active').count(),
        'completed_projects': Project.objects.filter(status='completed').count(),
        'planning_projects': Project.objects.filter(status='planning').count(),
    }
    
    # Task statistics
    task_stats = {
        'total_tasks': Task.objects.count(),
        'completed_tasks': Task.objects.filter(status='completed').count(),
        'in_progress_tasks': Task.objects.filter(status='in_progress').count(),
        'todo_tasks': Task.objects.filter(status='todo').count(),
    }
    
    context = {
        'user_stats': user_stats,
        'project_stats': project_stats,
        'task_stats': task_stats,
    }
    
    return render(request, 'accounts/reports.html', context)

@login_required
def logout_view(request):
    """Custom logout view with success message"""
    from django.contrib.auth import logout
    
    username = request.user.username
    logout(request)
    messages.success(request, f'You have been successfully logged out. See you again, {username}!')
    return redirect('accounts:login')
