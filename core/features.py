FEATURE_PACKAGES = {
    "drf": [
        "djangorestframework",
        "django-cors-headers",
        "djangorestframework-simplejwt"
    ],
    "pillow": [
        "Pillow"
    ],
    "whitenoise": [
        "whitenoise"
    ],
    "celery": [
        "celery",
        "django-celery-results"
    ],
    "redis": [
        "redis"
    ],
    "beat": [
        "django-celery-beat"
    ],
    "flower": [
        "flower"
    ]
}


def build_requirements(selected_features):

    # Base dependencies that every production Django project needs
    requirements = [
        "Django>=4.2,<5.0",
        "python-dotenv",
        "psycopg2-binary",
        "gunicorn"
    ]
    
    # Append selected feature packages in order
    for feature in selected_features:
        if feature in FEATURE_PACKAGES:
            requirements.extend(FEATURE_PACKAGES[feature])
            
    return "\n".join(requirements) + "\n"