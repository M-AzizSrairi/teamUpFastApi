# apiAuth/jwt_settings.py

from datetime import timedelta

SECRET_KEY = "5b50ce581cf0a8df1492d54b582811be716c697be76aa3c5c44fd4d7a75c01ac"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 120 

# Token expiration time for refresh tokens
REFRESH_TOKEN_EXPIRE_DAYS = 90
