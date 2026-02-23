"""
Django admin configuration for time_log models.
"""

from django.contrib import admin

from time_log.models import Project, Task, TimeLog


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    """Admin for Project — admin-managed; existing data may exist."""

    list_display = ["code", "name", "active", "created_at"]
    list_filter = ["active"]
    search_fields = ["name", "code"]


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    """Admin for Task — admin-managed; existing data may exist."""

    list_display = ["code", "name", "active", "created_at"]
    list_filter = ["active"]
    search_fields = ["name", "code"]


@admin.register(TimeLog)
class TimeLogAdmin(admin.ModelAdmin):
    """Admin for TimeLog."""

    list_display = ["user", "date", "project", "task", "time_spent", "billable", "created_at"]
    list_filter = ["billable", "project", "task"]
    search_fields = ["user__username", "description"]
    raw_id_fields = ["user", "project", "task"]
