import typer


def ask_features():

    features = []

    if typer.confirm("Include Django REST Framework?"):
        features.append("drf")

    if typer.confirm("Include Pillow?"):
        features.append("pillow")

    if typer.confirm("Include WhiteNoise?"):
        features.append("whitenoise")

    if typer.confirm("Include Celery?"):
        features.append("celery")

    if typer.confirm("Include Redis?"):
        features.append("redis")

    if typer.confirm("Include Celery Beat?"):
        features.append("beat")

    if typer.confirm("Include Flower?"):
        features.append("flower")

    if typer.confirm("Include Docker?", default=True):
        features.append("docker")

    if typer.confirm("Include Nginx?"):
        features.append("nginx")

    return features
