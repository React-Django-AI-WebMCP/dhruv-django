"""
DRF serializers for time_log: Project, Task, and TimeLog.
"""

import re
from datetime import timedelta

from rest_framework import serializers

from time_log.models import Project, Task, TimeLog


class ProjectSerializer(serializers.ModelSerializer):
    """Read-only serializer for Project (used in dropdowns and nested output)."""

    class Meta:
        model = Project
        fields = ["id", "name", "code"]


class TaskSerializer(serializers.ModelSerializer):
    """Read-only serializer for Task (used in dropdowns and nested output)."""

    class Meta:
        model = Task
        fields = ["id", "name", "code"]


class TimeLogCreateSerializer(serializers.Serializer):
    """Write serializer for creating a TimeLog.

    Accepts time_spent as HH:MM string and converts to timedelta.
    Required: project, task, time_spent.
    """

    date = serializers.DateField(required=False, allow_null=True)
    project = serializers.PrimaryKeyRelatedField(queryset=Project.objects.filter(active=True))
    task = serializers.PrimaryKeyRelatedField(queryset=Task.objects.filter(active=True))
    time_spent = serializers.CharField(max_length=5)
    description = serializers.CharField(required=False, allow_blank=True, default="")
    billable = serializers.BooleanField(required=False, default=False)

    def validate_time_spent(self, value: str) -> timedelta:
        """Parse HH:MM string into a timedelta."""
        pattern = re.compile(r"^\d{1,3}:\d{2}$")
        if not pattern.match(value):
            raise serializers.ValidationError("time_spent must be in HH:MM format (e.g. 01:30).")
        hours_str, minutes_str = value.split(":")
        hours = int(hours_str)
        minutes = int(minutes_str)
        if minutes >= 60:
            raise serializers.ValidationError("Minutes must be between 00 and 59.")
        return timedelta(hours=hours, minutes=minutes)


class TimeLogReadSerializer(serializers.ModelSerializer):
    """Read serializer for TimeLog — returned in API responses."""

    project = ProjectSerializer(read_only=True)
    task = TaskSerializer(read_only=True)
    time_spent = serializers.SerializerMethodField()

    class Meta:
        model = TimeLog
        fields = [
            "id",
            "user",
            "date",
            "project",
            "task",
            "time_spent",
            "description",
            "billable",
            "created_at",
            "updated_at",
        ]

    def get_time_spent(self, obj: TimeLog) -> str:
        """Return time_spent as HH:MM string."""
        total_seconds = int(obj.time_spent.total_seconds())
        hours, remainder = divmod(total_seconds, 3600)
        minutes = remainder // 60
        return f"{hours:02d}:{minutes:02d}"
