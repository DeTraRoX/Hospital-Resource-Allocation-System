from sqlalchemy import create_engine
from sqlmodel import Session
from urllib.parse import quote_plus
from .config import settings  # your Settings class from config.py

# --- Encode password safely ---
DB_PASSWORD_ENCODED = quote_plus(settings.DB_PASSWORD)

# --- Build the full PostgreSQL URL ---
DATABASE_URL = (
    f"postgresql+psycopg2://{settings.DB_USER}:{DB_PASSWORD_ENCODED}"
    f"@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}"
)

# --- Create SQLAlchemy engine ---
engine = create_engine(DATABASE_URL, echo=True, future=True)

# --- Dependency for FastAPI routes ---
def get_session():
    """
    Use this with FastAPI endpoints:
        session: Session = Depends(get_session)
    """
    with Session(engine) as session:
        yield session
