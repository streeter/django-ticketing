import os

SECRET_KEY = "django-ticketing-tests"
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
    }
}
if os.environ.get("TICKETING_TEST_MYSQL"):
    DATABASES["default"] = {
        "ENGINE": "django.db.backends.mysql",
        "NAME": os.environ.get("TICKETING_TEST_DB_NAME", "ticketing"),
        "USER": os.environ.get("TICKETING_TEST_DB_USER", "root"),
        "PASSWORD": os.environ.get("TICKETING_TEST_DB_PASSWORD", ""),
        "HOST": os.environ.get("TICKETING_TEST_DB_HOST", "127.0.0.1"),
        "PORT": os.environ.get("TICKETING_TEST_DB_PORT", "3306"),
        "OPTIONS": {"charset": "utf8mb4"},
    }
    mysql_version = os.environ.get("TOX_ENV_NAME", "").partition("-mysql-")[2]
    if mysql_version:
        port_variable = f"TICKETING_TEST_MYSQL_{mysql_version.replace('.', '_')}_PORT"
        DATABASES["default"]["PORT"] = os.environ.get(
            port_variable, DATABASES["default"]["PORT"]
        )
INSTALLED_APPS = ["ticketing"]
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
TICKETING_TESTING = True
