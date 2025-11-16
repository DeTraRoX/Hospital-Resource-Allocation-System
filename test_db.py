from app.db import engine

try:
    with engine.connect() as conn:
        print("✅ Connected to PostgreSQL successfully!")
except Exception as e:
    print("❌ Connection failed:", e)
