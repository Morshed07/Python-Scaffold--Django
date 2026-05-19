import os


def create_settings(project_name):

    settings_dir = "config/settings"

    os.makedirs(settings_dir, exist_ok=True)

    # Remove the auto-generated settings.py created by Django startproject
    if os.path.exists("config/settings.py"):
        os.remove("config/settings.py")

    # Create __init__.py that imports from the appropriate environment
    settings_init = """
import os
from .base import *

ENVIRONMENT = os.getenv("ENVIRONMENT", "development")

if ENVIRONMENT == "production":
    from .production import *
else:
    from .development import *
"""

    with open(f"{settings_dir}/__init__.py", "w") as f:
        f.write(settings_init)

    base = """
from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent.parent

SECRET_KEY = os.getenv("SECRET_KEY")

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
]

ROOT_URLCONF = "config.urls"

WSGI_APPLICATION = "config.wsgi.application"

STATIC_URL = "/static/"
"""

    development = """
from .base import *

DEBUG = True

ALLOWED_HOSTS = ["*"]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}
"""

    production = f"""
from .base import *
import os

DEBUG = False

ALLOWED_HOSTS = os.getenv(
    "ALLOWED_HOSTS",
    ""
).split(",")

DATABASES = {{
    "default": {{
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.getenv("POSTGRES_DB"),
        "USER": os.getenv("POSTGRES_USER"),
        "PASSWORD": os.getenv("POSTGRES_PASSWORD"),
        "HOST": os.getenv("POSTGRES_HOST"),
        "PORT": os.getenv("POSTGRES_PORT"),
    }}
}}
"""

    with open(f"{settings_dir}/base.py", "w") as f:
        f.write(base)

    with open(f"{settings_dir}/development.py", "w") as f:
        f.write(development)

    with open(f"{settings_dir}/production.py", "w") as f:
        f.write(production)