import os
import subprocess
import sys

def run_command(command, env=None):
    subprocess.run(command, shell=True, check=True, env=env)

def main():
    print("Hello Dev\n")

    # 1. Gather Inputs
    project_name = input("Project Name: ").strip().lower()
    if not project_name.isidentifier():
        print("Error: Project name must be a valid Python identifier (no spaces or hyphens).")
        sys.exit(1)

    use_celery = input("Include Celery + Redis + Flower? [y/N]: ").strip().lower() == 'y'
    use_pillow = input("Include Pillow (Image handling)? [y/N]: ").strip().lower() == 'y'

    print(f"\nScaffolding {project_name}... This will take a moment.\n")

    # 2. Create Project Directory & Virtual Environment
    os.makedirs(project_name, exist_ok=True)
    os.chdir(project_name)
    
    print("📦 Creating virtual environment...")
    run_command("python -m venv venv")
    
    if os.name == 'nt':
        python_exe = os.path.join("venv", "Scripts", "python")
        pip_exe = os.path.join("venv", "Scripts", "pip")
    else:
        python_exe = os.path.join("venv", "bin", "python")
        pip_exe = os.path.join("venv", "bin", "pip")

    # 3. Install Dependencies
    print("⬇️ Installing dependencies...")
    # psycopg2-binary added for PostgreSQL support out of the box
    packages = ["django", "python-dotenv", "gunicorn", "psycopg2-binary"]
    if use_celery:
        packages.extend(["celery", "redis", "flower"])
    if use_pillow:
        packages.append("Pillow")
        
    run_command(f"{pip_exe} install {' '.join(packages)}")
    run_command(f"{pip_exe} freeze > requirements.txt")

    # 4. Generate Django Project
    print("🏗️ Generating Django project...")
    run_command(f"{python_exe} -m django startproject {project_name} .")

    # 5. Refactor Settings
    print("⚙️ Setting up split settings (SQLite dev, PostgreSQL prod)...")
    settings_dir = os.path.join(project_name, "settings")
    os.makedirs(settings_dir, exist_ok=True)
    
    original_settings = os.path.join(project_name, "settings.py")
    with open(original_settings, "r") as f:
        settings_content = f.read()
    
    # Remove the default SQLite database config from base.py
    # We'll split this into dev and prod
    db_config_start = settings_content.find("DATABASES = {")
    db_config_end = settings_content.find("}", db_config_start) + 1
    if db_config_end > 0: # find the closing brace of the default db config
        db_config_end = settings_content.find("}", db_config_end) + 1
    
    settings_base_clean = settings_content[:db_config_start] + settings_content[db_config_end:]

    dotenv_setup = """
import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent.parent
load_dotenv(BASE_DIR / '.env.development')
"""
    settings_base_clean = settings_base_clean.replace(
        "from pathlib import Path", dotenv_setup
    ).replace(
        "BASE_DIR = Path(__file__).resolve().parent.parent", ""
    )

    with open(os.path.join(settings_dir, "base.py"), "w") as f:
        f.write(settings_base_clean)
        
    os.remove(original_settings)

    # SQLite for Development
    dev_settings = f"""from .base import *

DEBUG = True
ALLOWED_HOSTS = ['localhost', '127.0.0.1']

DATABASES = {{
    'default': {{
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }}
}}
"""
    with open(os.path.join(settings_dir, "development.py"), "w") as f:
        f.write(dev_settings)

    # PostgreSQL for Production
    prod_settings = f"""from .base import *
import os

DEBUG = False
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', '').split(',')

DATABASES = {{
    'default': {{
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('POSTGRES_DB', '{project_name}_db'),
        'USER': os.environ.get('POSTGRES_USER', 'postgres'),
        'PASSWORD': os.environ.get('POSTGRES_PASSWORD', 'postgres'),
        'HOST': os.environ.get('POSTGRES_HOST', 'db'),
        'PORT': os.environ.get('POSTGRES_PORT', '5432'),
    }}
}}
"""
    with open(os.path.join(settings_dir, "production.py"), "w") as f:
        f.write(prod_settings)

    open(os.path.join(settings_dir, "__init__.py"), "w").close()

    for entry_file in ["manage.py", os.path.join(project_name, "wsgi.py"), os.path.join(project_name, "asgi.py")]:
        with open(entry_file, "r") as f:
            content = f.read()
        content = content.replace(f"{project_name}.settings", f"{project_name}.settings.development")
        with open(entry_file, "w") as f:
            f.write(content)

    # 6. Create Environment Files
    print("🔐 Creating environment files...")
    with open(".env.development", "w") as f:
        f.write("SECRET_KEY='django-insecure-replace-this-later'\nDEBUG=True\n")
        
    with open(".env.production", "w") as f:
        f.write("SECRET_KEY='your-secure-production-key'\nDEBUG=False\nALLOWED_HOSTS=yourdomain.com,www.yourdomain.com\n")
        f.write(f"POSTGRES_DB={project_name}_db\nPOSTGRES_USER=postgres\nPOSTGRES_PASSWORD=supersecret\nPOSTGRES_HOST=db\nPOSTGRES_PORT=5432\n")

    # 7. Create Docker Setup (Ready for Postgres)
    print("🐳 Creating Docker configuration...")
    
    # Include libpq-dev for production postgres connections
    dockerfile = """FROM python:3.11-slim
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y libpq-dev gcc && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/
"""
    with open("Dockerfile", "w") as f:
        f.write(dockerfile)

    # Base docker-compose with PostgreSQL
    docker_compose = f"""version: '3.8'

services:
  db:
    image: postgres:15-alpine
    volumes:
      - postgres_data:/var/lib/postgresql/data
    environment:
      - POSTGRES_DB={project_name}_db
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=supersecret

  web:
    build: .
    command: >
      sh -c "python manage.py migrate &&
             python manage.py runserver 0.0.0.0:8000"
    volumes:
      - .:/app
    ports:
      - "8000:8000"
    env_file:
      - .env.production
    environment:
      - DJANGO_SETTINGS_MODULE={project_name}.settings.production
    depends_on:
      - db
"""
    # Add Celery/Redis if requested
    if use_celery:
        docker_compose += f"""
  redis:
    image: redis:alpine

  celery:
    build: .
    command: celery -A {project_name} worker -l info
    volumes:
      - .:/app
    env_file:
      - .env.production
    environment:
      - DJANGO_SETTINGS_MODULE={project_name}.settings.production
      - CELERY_BROKER_URL=redis://redis:6379/0
    depends_on:
      - db
      - redis
      - web
"""
    
    docker_compose += "\nvolumes:\n  postgres_data:\n"

    with open("docker-compose.yml", "w") as f:
        f.write(docker_compose)

    print("\n✅ Setup complete! Here is how to run it:\n")
    print("  Local Development (SQLite):")
    print(f"    cd {project_name}")
    print(f"    source venv/bin/activate")
    print(f"    python manage.py migrate")
    print(f"    python manage.py runserver\n")
    
    print("  Production/Docker (PostgreSQL):")
    print(f"    cd {project_name}")
    print(f"    docker-compose up --build\n")

if __name__ == "__main__":
    main()