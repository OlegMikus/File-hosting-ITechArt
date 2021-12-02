import os

from dotenv import load_dotenv

load_dotenv()

ENVIRONMENT = os.environ.get('ENVIRONMENT')

DJANGO_SECRET_KEY = os.environ.get('SECRET_KEY')
DATABASE_PASSWORD = os.environ.get('DATABASE_PASSWORD')
DATABASE_USER = os.environ.get('DATABASE_USER')
DATABASE_HOST = os.environ.get('DATABASE_HOST')
DATABASE_NAME = os.environ.get('DATABASE_NAME')
DATABASE_POST = os.environ.get('DATABASE_POST')
DJANGO_DEBUG_STATUS = os.environ.get('DJANGO_DEBUG_STATUS')
APP_TYPE = os.environ.get('APP_TYPE')
APP_TYPE_AUTH = os.environ.get('APP_TYPE_AUTH')
APP_TYPE_FILE = os.environ.get('APP_TYPE_FILE')

DJANGO_EMAIL_USE_TLS = os.environ.get('EMAIL_USE_TLS')
DJANGO_EMAIL_HOST = os.environ.get('EMAIL_HOST')
DJANGO_EMAIL_PORT = os.environ.get('EMAIL_PORT')
DJANGO_EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
DJANGO_EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')
DJANGO_DEFAULT_FROM_EMAIL = os.environ.get('DEFAULT_FROM_EMAIL')
