from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import datetime

# ✅ Hospital Model
class Hospital(SQLModel, table=True):
    id: Optional[int] = Field(default=1, primary_key=True)  # always hospital 1
    name: str = "Default Hospital"
    location: str = "Default City"
    total_beds: int = 100
    available_beds: int = 100
    ventilators: int = 20
    available_ventilators: int = 20

    requests: List["PatientRequest"] = Relationship(back_populates="hospital")
    allocations: List["Allocation"] = Relationship(back_populates="hospital")


# ✅ Patient Requests
class PatientRequest(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    condition: str
    requested_resource: str = "bed"
    status: str = "waiting"

    hospital_id: int = Field(default=1, foreign_key="hospital.id")  # auto = 1
    hospital: Optional[Hospital] = Relationship(back_populates="requests")


# ✅ Allocations
class Allocation(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    patient_id: int
    resource_type: str
    status: str = "active"
    allocated_at: datetime = Field(default_factory=datetime.utcnow)

    hospital_id: int = Field(default=1, foreign_key="hospital.id")  # auto = 1
    hospital: Optional[Hospital] = Relationship(back_populates="allocations")
