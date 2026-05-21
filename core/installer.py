import os
import subprocess
from core.runner import run
from core.features import FEATURE_PACKAGES
from core.settings import create_settings
from core.env import create_env
from core.docker import create_docker

def create_project(project_name, features):

    os.makedirs(project_name, exist_ok=True)
    os.chdir(project_name)

    print(f"\n🚀 Creating project: {project_name}\n")

    # venv
    subprocess.run(["python", "-m", "venv", "venv"])

    pip = "venv\\Scripts\\pip" if os.name == "nt" else "venv/bin/pip"
    python = "venv\\Scripts\\python" if os.name == "nt" else "venv/bin/python"

    packages = [
        "django",
        "python-dotenv",
        "gunicorn",
        "psycopg2-binary"
    ]

    for feature in features:
        if feature in FEATURE_PACKAGES:
            packages.extend(FEATURE_PACKAGES[feature])

    packages = list(set(packages))

    # install packages
    subprocess.run([pip, "install", *packages])

    # freeze requirements safely by piping stdout
    with open("requirements.txt", "w") as req:
        subprocess.run([pip, "freeze"], stdout=req)

    # django startproject
    subprocess.run([
        python,
        "-m",
        "django",
        "startproject",
        "config",
        "."
    ])

    # setup (Pass 'config' as the folder name since startproject created it)
    create_settings("config", features)
    create_env(project_name)

    if "docker" in features:
        create_docker(project_name, features)

    print("\n✅ Project created successfully!\n")
    print(" Take Love From Morshed Nayeem ❤️\n")

    print("Next steps:\n")
    if os.name == "nt":
        print("venv\\Scripts\\activate")
    else:
        print("source venv/bin/activate")

    print("python manage.py migrate")
    print("python manage.py runserver")