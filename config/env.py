import os
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
DB_MYSQL_HOST = os.getenv("DB_MYSQL_HOST")
DB_MYSQL_PORT = os.getenv("DB_MYSQL_PORT")
DB_MYSQL_NAME = os.getenv("DB_MYSQL_NAME")
DB_MYSQL_USER = os.getenv("DB_MYSQL_USER")
DB_MYSQL_PASS = os.getenv("DB_MYSQL_PASS")