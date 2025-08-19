from sqlalchemy import create_engine
from .config import settings
from urllib.parse import quote_plus

DB_PASSWORD_ENCODED = quote_plus(settings.DB_PASSWORD)
DATABASE_URL = f"postgresql+psycopg2://{settings.DB_USER}:{DB_PASSWORD_ENCODED}@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}"
engine = create_engine(DATABASE_URL)
