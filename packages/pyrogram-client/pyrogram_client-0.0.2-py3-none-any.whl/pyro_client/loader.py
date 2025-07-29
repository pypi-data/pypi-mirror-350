from dotenv import load_dotenv
from os import getenv as env

load_dotenv()

API_ID = env("API_ID")
API_HASH = env("API_HASH")
PG_DSN = f"postgres://{env('POSTGRES_USER')}:{env('POSTGRES_PASSWORD')}@{env('POSTGRES_HOST', 'xyncdbs')}:" \
         f"{env('POSTGRES_PORT', 5432)}/{env('POSTGRES_DB', env('POSTGRES_USER'))}"
TOKEN = env("TOKEN")
WSToken = env("WST")
