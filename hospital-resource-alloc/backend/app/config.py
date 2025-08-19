from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DB_USER: str = "ayush"
    DB_PASSWORD: str = "AyushDobhal@123"  # or your actual password
    DB_HOST: str = "localhost"
    DB_PORT: str = "5432"
    DB_NAME: str = "hospital_db"
settings = Settings()
