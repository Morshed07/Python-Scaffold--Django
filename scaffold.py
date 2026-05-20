import typer
from rich import print
from rich.prompt import Prompt  # <-- 1. Import Prompt from rich

from core.prompts import ask_features
from core.installer import create_project

app = typer.Typer()


WELCOME_MESSAGE = """
[bold cyan]
╔══════════════════════════════════════════════╗
║                                              ║
║        🚀 Django Scaffold CLI 🚀             ║
║                                              ║
║  Production-ready Django project starter     ║
║                                              ║
╚══════════════════════════════════════════════╝
[/bold cyan]

[green]Features:[/green]
  ✅ Django Production Setup
  ✅ Docker & PostgreSQL
  ✅ Celery + Redis + Flower
  ✅ Environment Separation
  ✅ Clean Scalable Structure

[bold yellow]Happy Coding, Developer! 👨‍💻[/bold yellow]
"""


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

    print(WELCOME_MESSAGE)

    # Ask project name if not provided
    if not name:
        # 2. Use Prompt.ask instead of typer.prompt
        name = Prompt.ask("[cyan]Project name[/cyan]")

    # Ask feature prompts if not provided
    if not features:
        features = ask_features()

    create_project(
        project_name=name,
        features=features
    )


if __name__ == "__main__":
    app()