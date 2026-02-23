"""
Service layer for time_log — keeps business logic out of views.
"""

import logging

from django.contrib.auth.models import AbstractBaseUser

from time_log.models import TimeLog

logger = logging.getLogger(__name__)


def create_time_log(user: AbstractBaseUser, validated_data: dict) -> TimeLog:
    """Create and persist a new TimeLog for the given user.

    Args:
        user: The authenticated user creating the log.
        validated_data: Cleaned data from TimeLogCreateSerializer
                        (time_spent already converted to timedelta).

    Returns:
        The newly created TimeLog instance.
    """
    time_log = TimeLog.objects.create(user=user, **validated_data)
    logger.info("TimeLog created: id=%s user=%s date=%s", time_log.id, user.pk, time_log.date)
    return time_log
