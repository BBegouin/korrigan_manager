from korrigan_manager.base_settings import *

DEBUG = False

# Domains for public site
ALLOWED_HOSTS = ["korrigan.bloodbowlclub.com"]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": "kmng",
        "USER": "root",
        "PASSWORD": os.environ.get('DB_PWD',''),
        "HOST": "localhost",   # Or an IP Address that your DB is hosted on
        "PORT": "3306",
    }
}