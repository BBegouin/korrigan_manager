from korrigan_manager.base_settings import *

DEBUG = True

# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": "kmng",
        "USER": "root",
        "PASSWORD": "root",
        "HOST": "localhost",   # Or an IP Address that your DB is hosted on
        "PORT": "3306",
        "OPTIONS":{'init_command': "SET sql_mode='STRICT_TRANS_TABLES'"},
    }
}
