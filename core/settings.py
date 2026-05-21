import os

def create_settings(project_name):
    settings_dir = "config/settings"
    os.makedirs(settings_dir, exist_ok=True)

    # Make development the default fallback so manage.py works out of the box
    with open(f"{settings_dir}/__init__.py", "w") as f:
        f.write("from .development import *\n")

    base = """from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Don't load_dotenv here, let the environment-specific files handle it
SECRET_KEY = os.getenv("SECRET_KEY", "fallback-insecure-key-for-dev")

DEBUG = False

ALLOWED_HOSTS = []

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    # ==========================
    # Third-party apps go here
    # ==========================
    "rest_framework",
    "corsheaders",
    "rest_framework_simplejwt",


    # ==========================
    # Installed apps go here
    # ==========================
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
"""

    development = """import os
from pathlib import Path
from dotenv import load_dotenv

# Calculate BASE_DIR here to load the right .env file BEFORE importing base
BASE_DIR = Path(__file__).resolve().parent.parent.parent
load_dotenv(BASE_DIR / ".env.development")

# Now import base (it will use the env vars we just loaded)
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

    production = """import os
from pathlib import Path
from dotenv import load_dotenv

# Load production env BEFORE importing base
BASE_DIR = Path(__file__).resolve().parent.parent.parent
load_dotenv(BASE_DIR / ".env.production")

from .base import *

DEBUG = False

# Safely split hosts, ignoring empty strings
env_hosts = os.getenv("ALLOWED_HOSTS", "")
ALLOWED_HOSTS = [host.strip() for host in env_hosts.split(",") if host.strip()]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.getenv("POSTGRES_DB"),
        "USER": os.getenv("POSTGRES_USER"),
        "PASSWORD": os.getenv("POSTGRES_PASSWORD"),
        "HOST": os.getenv("POSTGRES_HOST", "db"),
        "PORT": os.getenv("POSTGRES_PORT", "5432"),
    }
}
"""

    with open(f"{settings_dir}/base.py", "w") as f:
        f.write(base)

    with open(f"{settings_dir}/development.py", "w") as f:
        f.write(development)

    with open(f"{settings_dir}/production.py", "w") as f:
        f.write(production)


import os
import secrets
from pathlib import Path

def generate_django_project(project_name="core"):
    """Generates a complete 12-factor Django REST project structure."""
    
    # 1. Define Directories
    base_dir = Path.cwd()
    project_dir = base_dir / project_name
    settings_dir = project_dir / "settings"
    
    os.makedirs(settings_dir, exist_ok=True)

    # 2. Generate secure random keys
    dev_secret = secrets.token_urlsafe(50)
    
    # ==========================================
    # FILE TEMPLATES
    # ==========================================
    
    env_dev = f"""SECRET_KEY={dev_secret}
DEBUG=True
ALLOWED_HOSTS=*
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
CSRF_TRUSTED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
"""

    env_prod = """SECRET_KEY=generate_a_secure_key_here
DEBUG=False
ALLOWED_HOSTS=api.yourdomain.com,www.yourdomain.com
CORS_ALLOWED_ORIGINS=https://yourfrontend.com,https://www.yourfrontend.com
CSRF_TRUSTED_ORIGINS=https://yourfrontend.com,https://www.yourfrontend.com

POSTGRES_DB=mydb
POSTGRES_USER=myuser
POSTGRES_PASSWORD=mypassword
POSTGRES_HOST=db
POSTGRES_PORT=5432
"""

    requirements = """Django>=4.2,<5.0
djangorestframework
django-cors-headers
djangorestframework-simplejwt
python-dotenv
psycopg2-binary
gunicorn
"""

    manage_py = """#!/usr/bin/env python
import os
import sys

def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', '<PROJECT_NAME>.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed?"
        ) from exc
    execute_from_command_line(sys.argv)

if __name__ == '__main__':
    main()
"""

    urls_py = """from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('api/v1/', include('your_app.urls')),
]
"""

    wsgi_py = """import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', '<PROJECT_NAME>.settings')
application = get_wsgi_application()
"""

    asgi_py = """import os
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', '<PROJECT_NAME>.settings')
application = get_asgi_application()
"""

    base_settings = """from pathlib import Path
import os
from datetime import timedelta

BASE_DIR = Path(__file__).resolve().parent.parent.parent
SECRET_KEY = os.getenv("SECRET_KEY", "fallback-insecure-key-for-dev")
DEBUG = False
ALLOWED_HOSTS = []

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # ==========================
    # Third-party apps go here
    # ==========================
    "rest_framework",
    "corsheaders",
    "rest_framework_simplejwt",


    # ==========================
    # Installed apps go here
    # ==========================
    # "accounts",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "<PROJECT_NAME>.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "<PROJECT_NAME>.wsgi.application"

LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
MEDIA_URL = "media/"
MEDIA_ROOT = BASE_DIR / "media"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# ==========================================
# CORS & CSRF Configuration
# ==========================================
env_cors = os.getenv("CORS_ALLOWED_ORIGINS", "")
CORS_ALLOWED_ORIGINS = [origin.strip() for origin in env_cors.split(",") if origin.strip()]

env_csrf = os.getenv("CSRF_TRUSTED_ORIGINS", "")
CSRF_TRUSTED_ORIGINS = [origin.strip() for origin in env_csrf.split(",") if origin.strip()]

# ==========================================
# REST Framework & JWT Configuration
# ==========================================
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ]
}

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(days=7),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=30),
}
"""

    dev_settings = """from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent.parent
load_dotenv(BASE_DIR / ".env.development")

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

    prod_settings = """import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent.parent
load_dotenv(BASE_DIR / ".env.production")

from .base import *

DEBUG = False
env_hosts = os.getenv("ALLOWED_HOSTS", "")
ALLOWED_HOSTS = [host.strip() for host in env_hosts.split(",") if host.strip()]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.getenv("POSTGRES_DB"),
        "USER": os.getenv("POSTGRES_USER"),
        "PASSWORD": os.getenv("POSTGRES_PASSWORD"),
        "HOST": os.getenv("POSTGRES_HOST", "db"),
        "PORT": os.getenv("POSTGRES_PORT", "5432"),
    }
}
"""

    # ==========================================
    # FILE WRITER HELPER
    # ==========================================
    def write_file(path, content):
        parsed_content = content.replace("<PROJECT_NAME>", project_name)
        with open(path, "w") as f:
            f.write(parsed_content)
        print(f"Created: {path}")

    # ==========================================
    # EXECUTE GENERATION
    # ==========================================
    write_file(base_dir / ".env.development", env_dev)
    write_file(base_dir / ".env.production", env_prod)
    write_file(base_dir / "requirements.txt", requirements)
    write_file(base_dir / "manage.py", manage_py)
    
    os.chmod(base_dir / "manage.py", 0o755)

    write_file(project_dir / "__init__.py", "")
    write_file(project_dir / "urls.py", urls_py)
    write_file(project_dir / "wsgi.py", wsgi_py)
    write_file(project_dir / "asgi.py", asgi_py)

    write_file(settings_dir / "__init__.py", "from .development import *\n")
    write_file(settings_dir / "base.py", base_settings)
    write_file(settings_dir / "development.py", dev_settings)
    write_file(settings_dir / "production.py", prod_settings)

    print(f"\n✅ Successfully scaffolded {project_name}!")

if __name__ == "__main__":
    import sys
    name = sys.argv[1] if len(sys.argv) > 1 else "config"
    generate_django_project(name)