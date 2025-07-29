# django-env-checker

**django-env-checker** is a simple yet effective tool to enforce required environment variables in your Django project.
If any required environment variables are missing, the application will raise an error.

---

## Installation

```bash
pip install django-env-checker
```

### settings.py
Add ```env_check``` to your ```INSTALLED_APPS```

Define the list of required environment variables:

```
REQUIRED_ENV_VARS = [
    'SECRET_KEY',
    'API_KEY',
    'PGPASSWORD'
]
```
Run your application with DEBUG = False to activate the environment variable checks.
If any required environment variable is missing, the app will raise an error on startup.

---

## Behavior

The environment variable validation only runs when DEBUG is set to False.

If a required variable is missing, the startup will fail immediately, preventing the app from running in an unsafe state.