from django.contrib import admin
from .models import Task, TaskComment

class TaskCommentInline(admin.TabularInline):
    model = TaskComment
    extra = 0
    readonly_fields = ('created_at',)

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'project', 'assigned_to', 'priority', 'status', 'due_date', 'created_at')
    list_filter = ('status', 'priority', 'project', 'created_at', 'due_date')
    search_fields = ('title', 'description', 'assigned_to__username', 'project__name')
    date_hierarchy = 'created_at'
    readonly_fields = ('created_at', 'updated_at')
    inlines = [TaskCommentInline]
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'description', 'project')
        }),
        ('Assignment & Priority', {
            'fields': ('assigned_to', 'created_by', 'priority', 'status')
        }),
        ('Timeline', {
            'fields': ('due_date',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

@admin.register(TaskComment)
class TaskCommentAdmin(admin.ModelAdmin):
    list_display = ('task', 'user', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('task__title', 'user__username', 'comment')
    readonly_fields = ('created_at',)
