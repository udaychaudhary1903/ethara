from django import forms
from django.db import models
from .models import Task, TaskComment
from projects.models import Project
from accounts.models import User

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ('title', 'description', 'project', 'assigned_to', 'priority', 'status', 'due_date')
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'project': forms.Select(attrs={'class': 'form-control'}),
            'assigned_to': forms.Select(attrs={'class': 'form-control'}),
            'priority': forms.Select(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'due_date': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
        }
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        if user:
            if user.is_admin:
                # Admin can assign tasks to any project and any user
                self.fields['project'].queryset = Project.objects.all()
                self.fields['assigned_to'].queryset = User.objects.filter(is_active=True)
            else:
                # Manager can only assign tasks to their projects and team members
                user_projects = Project.objects.filter(
                    models.Q(created_by=user) | models.Q(assigned_users=user)
                ).distinct()
                self.fields['project'].queryset = user_projects
                
                # Get users from these projects
                project_users = User.objects.filter(
                    models.Q(assigned_projects__in=user_projects) | 
                    models.Q(role__in=['manager', 'user'])
                ).filter(is_active=True).distinct()
                self.fields['assigned_to'].queryset = project_users

class TaskCommentForm(forms.ModelForm):
    class Meta:
        model = TaskComment
        fields = ('comment',)
        widgets = {
            'comment': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Add a comment...'
            })
        }

class TaskStatusForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ('status',)
        widgets = {
            'status': forms.Select(attrs={'class': 'form-control'})
        }

class TaskFilterForm(forms.Form):
    search = forms.CharField(
        max_length=200,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Search tasks...'
        })
    )
    project = forms.ModelChoiceField(
        queryset=Project.objects.all(),
        required=False,
        empty_label="All Projects",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    assigned_to = forms.ModelChoiceField(
        queryset=User.objects.filter(is_active=True),
        required=False,
        empty_label="All Users",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    status = forms.ChoiceField(
        choices=[('', 'All Statuses')] + Task.STATUS_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    priority = forms.ChoiceField(
        choices=[('', 'All Priorities')] + Task.PRIORITY_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
