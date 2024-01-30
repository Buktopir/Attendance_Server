import os
from dotenv import load_dotenv

load_dotenv()
G_CLIENT_SECRET = os.environ.get("G_CLIENT_SECRET")
G_CLIENT_ID = os.environ.get("G_CLIENT_ID")
SECRET = os.environ.get("SECRET")

DB_HOST = os.environ.get('DB_HOST')
DB_PORT = os.environ.get('DB_PORT')
DB_USER = os.environ.get('DB_USER')
DB_PASS = os.environ.get('DB_PASS')
DB_NAME = os.environ.get('DB_NAME')

IP = os.environ.get('IP')
PORT = os.environ.get('PORT')

POSTGRES_URI = f'postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
