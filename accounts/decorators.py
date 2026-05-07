from django.http import HttpResponseForbidden
from django.shortcuts import redirect
from django.contrib import messages
from functools import wraps

def admin_required(view_func):
    """
    Decorator for views that checks that the user is an admin.
    """
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('accounts:login')
        if not request.user.is_admin:
            messages.error(request, 'You do not have permission to access this page.')
            return redirect('dashboard')
        return view_func(request, *args, **kwargs)
    return _wrapped_view

def manager_required(view_func):
    """
    Decorator for views that checks that the user is a manager or admin.
    """
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('accounts:login')
        if not (request.user.is_manager or request.user.is_admin):
            messages.error(request, 'You do not have permission to access this page.')
            return redirect('dashboard')
        return view_func(request, *args, **kwargs)
    return _wrapped_view

def user_required(view_func):
    """
    Decorator for views that checks that the user is authenticated (any role).
    """
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('accounts:login')
        return view_func(request, *args, **kwargs)
    return _wrapped_view

class AdminRequiredMixin:
    """
    Mixin for class-based views that checks that the user is an admin.
    """
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('accounts:login')
        if not request.user.is_admin:
            messages.error(request, 'You do not have permission to access this page.')
            return redirect('dashboard')
        return super().dispatch(request, *args, **kwargs)

class ManagerRequiredMixin:
    """
    Mixin for class-based views that checks that the user is a manager or admin.
    """
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('accounts:login')
        if not (request.user.is_manager or request.user.is_admin):
            messages.error(request, 'You do not have permission to access this page.')
            return redirect('dashboard')
        return super().dispatch(request, *args, **kwargs)
