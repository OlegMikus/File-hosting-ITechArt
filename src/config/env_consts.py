import os

from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.environ.get('SECRET_KEY')
DATABASE_PASSWORD = os.environ.get('DATABASE_PASSWORD')
DATABASE_USER = os.environ.get('DATABASE_USER')
DATABASE_HOST = os.environ.get('DATABASE_HOST')
DATABASE_NAME = os.environ.get('DATABASE_NAME')
DATABASE_POST = os.environ.get('DATABASE_POST')

ENV_CONSTS = {
    'SECRET_KEY': SECRET_KEY,
    'DATABASE_PASSWORD': DATABASE_PASSWORD,
    'DATABASE_USER': DATABASE_USER,
    'DATABASE_HOST': DATABASE_HOST,
    'DATABASE_NAME': DATABASE_NAME,
    'DATABASE_POST': DATABASE_POST
}
