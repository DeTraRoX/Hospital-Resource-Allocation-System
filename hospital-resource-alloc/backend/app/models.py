from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime

# --------------------------
# Hospital Model
# --------------------------
class Hospital(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    capacity: int

# --------------------------
# Request Model
# --------------------------
class Request(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    hospital_id: int
    resource: str
    quantity: int
    created_at: datetime = Field(default_factory=datetime.utcnow)

# --------------------------
# Allocation Model
# --------------------------
class Allocation(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    request_id: int
    hospital_id: int
    quantity_allocated: int
    allocated_at: datetime = Field(default_factory=datetime.utcnow)
