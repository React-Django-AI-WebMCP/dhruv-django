"""
Logging configuration. Configure handlers (file, console) and formatters in settings.
"""
import logging

# Project logger; attach handlers in config/settings/base.py or local.py
logger = logging.getLogger("core")
