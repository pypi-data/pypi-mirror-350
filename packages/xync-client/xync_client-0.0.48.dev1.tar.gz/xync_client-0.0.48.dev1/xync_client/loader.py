from dotenv import load_dotenv
from os import getenv as env

load_dotenv()

if not (TOKEN := env("TOKEN")):
    import logging

    load_dotenv("/api/.env")
    logging.info(TOKEN := env("TOKEN"))

PG_DSN = f"postgres://{env('POSTGRES_USER')}:{env('POSTGRES_PASSWORD')}@{env('POSTGRES_HOST', 'xyncdbs')}:{env('POSTGRES_PORT', 5432)}/{env('POSTGRES_DB', env('POSTGRES_USER'))}"
TG_API_ID = env("TG_API_ID")
TG_API_HASH = env("TG_API_HASH")
WSToken = env("WST")
