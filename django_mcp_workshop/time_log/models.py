"""
Models for the time_log app: Project, Task, TimeLog.
"""

from django.conf import settings
from django.db import models

from core.models import TimeStampedModel


class Project(TimeStampedModel):
    """A project that time can be logged against."""

    name = models.CharField(max_length=255)
    code = models.CharField(max_length=50)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ["name"]

    def __str__(self) -> str:
        return f"{self.code} — {self.name}"


class Task(TimeStampedModel):
    """A task within a project that time can be logged against."""

    name = models.CharField(max_length=255)
    code = models.CharField(max_length=50)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ["name"]

    def __str__(self) -> str:
        return f"{self.code} — {self.name}"


class TimeLog(TimeStampedModel):
    """A single time log entry recorded by a user."""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="time_logs",
    )
    date = models.DateField()
    project = models.ForeignKey(
        Project,
        on_delete=models.PROTECT,
        related_name="time_logs",
    )
    task = models.ForeignKey(
        Task,
        on_delete=models.PROTECT,
        related_name="time_logs",
    )
    time_spent = models.DurationField()
    description = models.TextField(blank=True, default="")
    billable = models.BooleanField(default=False)

    class Meta:
        ordering = ["-date", "-created_at"]

    def __str__(self) -> str:
        return f"{self.user} | {self.date} | {self.project.code} | {self.time_spent}"
