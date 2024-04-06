"""
This file maintain all type configration and settings need as per environment.
"""

# Django
SECRET_KEY = 'django-insecure-fiir2nh-2ji@mf1pwe^yr*abo1mvna^_u9vv=2upthhbd#u@q-'
ALLOWED_HOSTS = []
DEBUG = True

# Database
DB_NAME = 'auction_plaza'
DB_HOST = 'localhost'
DB_PORT = '5432'
DB_USERNAME = 'postgres'
DB_PASSWORD = 'admin'

# Redis
REDIS_LOCATION = 'redis://127.0.0.1:6379/1'
