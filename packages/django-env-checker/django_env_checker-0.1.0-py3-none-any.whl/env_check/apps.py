from django.apps import AppConfig
from django.core.exceptions import ImproperlyConfigured
from typing import List
import os


class EnvCheckConfig(AppConfig):
    name = "env_check"
    verbose_name = "Environment Variable Checker"

    def ready(self) -> None:
        from .checks import check_env_vars
        check_env_vars()
