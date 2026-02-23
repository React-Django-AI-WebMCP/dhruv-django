"""
API views for time_log: TimeLog creation, Project list, Task list.
"""

import logging

from rest_framework import generics, mixins, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from core.responses import success_response
from time_log.models import Project, Task
from time_log.serializers import ProjectSerializer, TaskSerializer, TimeLogCreateSerializer, TimeLogReadSerializer
from time_log.services import create_time_log

logger = logging.getLogger(__name__)


class TimeLogViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    """POST /api/time-logs/ — create a new time log for the authenticated user."""

    permission_classes = [IsAuthenticated]
    serializer_class = TimeLogCreateSerializer

    def create(self, request: Request, *args: object, **kwargs: object) -> Response:
        """Validate request, persist time log via service, return 201."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        time_log = create_time_log(user=request.user, validated_data=serializer.validated_data)
        read_serializer = TimeLogReadSerializer(time_log)
        return success_response(data=read_serializer.data, message="Time log created.", status_code=201)


class ProjectListView(generics.ListAPIView):
    """GET /api/projects/ — list active projects for dropdown population."""

    permission_classes = [IsAuthenticated]
    serializer_class = ProjectSerializer
    queryset = Project.objects.filter(active=True)


class TaskListView(generics.ListAPIView):
    """GET /api/tasks/ — list active tasks for dropdown population."""

    permission_classes = [IsAuthenticated]
    serializer_class = TaskSerializer
    queryset = Task.objects.filter(active=True)
