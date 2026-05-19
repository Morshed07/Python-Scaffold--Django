def create_env(project_name):

    development = """
SECRET_KEY=dev-secret-key
DEBUG=True
"""

    production = f"""
SECRET_KEY=change-me
DEBUG=False

ALLOWED_HOSTS=localhost,127.0.0.1

POSTGRES_DB={project_name}_db
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_HOST=db
POSTGRES_PORT=5432
"""

    with open(".env.development", "w") as f:
        f.write(development)

    with open(".env.production", "w") as f:
        f.write(production)