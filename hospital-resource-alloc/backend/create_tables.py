from sqlmodel import SQLModel
from app.db import engine
from app.models import Hospital, Request, Allocation

def create_all_tables():
    SQLModel.metadata.create_all(engine)
    print("✅ All tables created successfully")

if __name__ == "__main__":
    create_all_tables()
