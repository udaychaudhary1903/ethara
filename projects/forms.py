from django import forms
from .models import Project
from accounts.models import User

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ('name', 'description', 'status', 'assigned_users', 'start_date', 'end_date')
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'assigned_users': forms.SelectMultiple(attrs={'class': 'form-control', 'size': 8}),
            'start_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'end_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        # Filter assigned users based on current user's role
        if user:
            if user.is_admin:
                # Admin can assign any active user
                self.fields['assigned_users'].queryset = User.objects.filter(is_active=True)
            else:
                # Manager can only assign managers and regular users
                self.fields['assigned_users'].queryset = User.objects.filter(
                    is_active=True, 
                    role__in=['manager', 'user']
                )
        else:
            self.fields['assigned_users'].queryset = User.objects.filter(is_active=True)

class ProjectFilterForm(forms.Form):
    search = forms.CharField(
        max_length=200,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Search projects...'
        })
    )
    status = forms.ChoiceField(
        choices=[('', 'All Statuses')] + Project.STATUS_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
