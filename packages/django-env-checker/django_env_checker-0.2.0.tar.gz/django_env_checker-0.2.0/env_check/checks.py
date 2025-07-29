from django.core.exceptions import ImproperlyConfigured
import os
from typing import List


def check_env_vars() -> None:
    required_vars: List[str] = get_required_env_vars()
    missing_vars = [var for var in required_vars if not os.getenv(var)]

    if missing_vars:
        raise ImproperlyConfigured(
            f"Missing required environment variables: {', '.join(missing_vars)}"
        )


def get_required_env_vars() -> List[str]:
    """
    Return the list of required environment variables.
    Override this or configure in settings by the user.
    """
    # Default vars - can be overridden
    from django.conf import settings

    return getattr(settings, "REQUIRED_ENV_VARS", [])
