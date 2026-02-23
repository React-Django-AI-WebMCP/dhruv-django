"""
URL routing for time_log app.

Endpoints:
    POST   /api/time-logs/   — create a new time log
    GET    /api/projects/    — list active projects (for dropdown)
    GET    /api/tasks/       — list active tasks (for dropdown)
"""

from django.urls import path
from rest_framework.routers import DefaultRouter

from time_log.views import ProjectListView, TaskListView, TimeLogViewSet

router = DefaultRouter()
router.register("time-logs", TimeLogViewSet, basename="time-log")

urlpatterns = router.urls + [
    path("projects/", ProjectListView.as_view(), name="project-list"),
    path("tasks/", TaskListView.as_view(), name="task-list"),
]
