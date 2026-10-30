SECRET_KEY = "django-ticketing-tests"
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
    }
}
INSTALLED_APPS = ["ticketing"]
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
TICKETING_TESTING = True
