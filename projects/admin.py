from django.contrib import admin
from .models import Project

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'status', 'created_by', 'start_date', 'end_date', 'created_at')
    list_filter = ('status', 'created_at', 'start_date', 'end_date')
    search_fields = ('name', 'description', 'created_by__username')
    filter_horizontal = ('assigned_users',)
    date_hierarchy = 'created_at'
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'description', 'status')
        }),
        ('Assignment', {
            'fields': ('created_by', 'assigned_users')
        }),
        ('Timeline', {
            'fields': ('start_date', 'end_date')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
