from korrigan_manager.base_settings import *

DEBUG = False

FRONT_DOMAIN = "localhost:5555"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": "BBClub",
        "USER": "root",
        "PASSWORD": os.environ.get('DB_PWD',''),
        "HOST": "localhost",   # Or an IP Address that your DB is hosted on
        "PORT": "3306",
    }
}