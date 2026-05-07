from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.urls import reverse_lazy
from django.db.models import Q, Count
from django.utils.decorators import method_decorator
from django.http import JsonResponse

from .models import Project
from .forms import ProjectForm
from accounts.decorators import manager_required, admin_required, ManagerRequiredMixin
from accounts.models import User
from tasks.models import Task

# Manager and Admin views
@method_decorator([login_required, manager_required], name='dispatch')
class ProjectListView(ListView):
    model = Project
    template_name = 'projects/project_list.html'
    context_object_name = 'projects'
    paginate_by = 20
    
    def get_queryset(self):
        user = self.request.user
        
        if user.is_admin:
            # Admin can see all projects
            queryset = Project.objects.all()
        else:
            # Manager can see projects they created or are assigned to
            queryset = Project.objects.filter(
                Q(created_by=user) | Q(assigned_users=user)
            ).distinct()
        
        # Apply filters
        search = self.request.GET.get('search')
        status = self.request.GET.get('status')
        
        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) | Q(description__icontains=search)
            )
        
        if status:
            queryset = queryset.filter(status=status)
        
        return queryset.order_by('-created_at')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search'] = self.request.GET.get('search', '')
        context['selected_status'] = self.request.GET.get('status', '')
        context['status_choices'] = Project.STATUS_CHOICES
        return context

@method_decorator([login_required, manager_required], name='dispatch')
class ProjectDetailView(DetailView):
    model = Project
    template_name = 'projects/project_detail.html'
    context_object_name = 'project'
    
    def get_queryset(self):
        user = self.request.user
        if user.is_admin:
            return Project.objects.all()
        else:
            return Project.objects.filter(
                Q(created_by=user) | Q(assigned_users=user)
            ).distinct()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        project = self.get_object()
        context['tasks'] = project.tasks.all().order_by('-created_at')
        context['team_members'] = project.assigned_users.all()
        return context

@method_decorator([login_required, manager_required], name='dispatch')
class ProjectCreateView(CreateView):
    model = Project
    form_class = ProjectForm
    template_name = 'projects/project_form.html'
    success_url = reverse_lazy('projects:project_list')
    
    def form_valid(self, form):
        form.instance.created_by = self.request.user
        messages.success(self.request, 'Project created successfully!')
        return super().form_valid(form)

@method_decorator([login_required, manager_required], name='dispatch')
class ProjectUpdateView(UpdateView):
    model = Project
    form_class = ProjectForm
    template_name = 'projects/project_form.html'
    success_url = reverse_lazy('projects:project_list')
    
    def get_queryset(self):
        user = self.request.user
        if user.is_admin:
            return Project.objects.all()
        else:
            return Project.objects.filter(created_by=user)
    
    def form_valid(self, form):
        messages.success(self.request, 'Project updated successfully!')
        return super().form_valid(form)

@method_decorator([login_required, manager_required], name='dispatch')
class ProjectDeleteView(DeleteView):
    model = Project
    template_name = 'projects/project_confirm_delete.html'
    success_url = reverse_lazy('projects:project_list')
    
    def get_queryset(self):
        user = self.request.user
        if user.is_admin:
            return Project.objects.all()
        else:
            return Project.objects.filter(created_by=user)
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Project deleted successfully!')
        return super().delete(request, *args, **kwargs)

@login_required
@manager_required
def assign_users_to_project(request, pk):
    """AJAX view to assign users to a project"""
    project = get_object_or_404(Project, pk=pk)
    
    # Check permissions
    user = request.user
    if not user.is_admin and project.created_by != user:
        return JsonResponse({'error': 'Permission denied'}, status=403)
    
    if request.method == 'POST':
        user_ids = request.POST.getlist('user_ids')
        project.assigned_users.set(user_ids)
        
        return JsonResponse({
            'success': True,
            'message': f'Successfully assigned {len(user_ids)} users to the project.'
        })
    
    # Get available users (exclude admins unless current user is admin)
    if user.is_admin:
        available_users = User.objects.filter(is_active=True)
    else:
        available_users = User.objects.filter(is_active=True, role__in=['manager', 'user'])
    
    assigned_users = project.assigned_users.all()
    
    context = {
        'project': project,
        'available_users': available_users,
        'assigned_users': assigned_users,
    }
    
    return render(request, 'projects/assign_users.html', context)
