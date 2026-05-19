import os
from jinja2 import Environment, FileSystemLoader


def create_docker(project_name, features):
    # Get the absolute path to the templates directory
    templates_dir = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        "templates"
    )

    env = Environment(
        loader=FileSystemLoader(templates_dir)
    )

    dockerfile_template = env.get_template("Dockerfile.j2")

    with open("Dockerfile", "w") as f:
        f.write(
            dockerfile_template.render()
        )

    compose_template = env.get_template("docker-compose.j2")

    with open("docker-compose.yml", "w") as f:
        f.write(
            compose_template.render(
                project_name=project_name,
                features=features
            )
        )

    entry_template = env.get_template("entrypoint.sh.j2")

    with open("entrypoint.sh", "w") as f:
        f.write(entry_template.render())