import typer

from core.prompts import ask_features
from core.installer import create_project

app = typer.Typer()


@app.command()
def main(
    name: str = typer.Argument(
        None,
        help="Project name"
    ),

    features: list[str] = typer.Option(
        None,
        "--features",
        "-f",
        help="Optional features"
    )
):

    # Ask project name if not provided
    if not name:
        name = typer.prompt("Project name")

    # Ask feature prompts if not provided
    if not features:
        features = ask_features()

    create_project(
        project_name=name,
        features=features
    )


if __name__ == "__main__":
    app()