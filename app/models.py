from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import datetime, timezone, timedelta


# ✅ Define IST timezone
IST = timezone(timedelta(hours=5, minutes=30))


# ----------------------------------------------------
# Base mixin for dict conversion
# ----------------------------------------------------
class BaseModel(SQLModel):
    class Config:
        orm_mode = True

    def to_dict(self, include_relationships: bool = False):
        data = self.dict()
        if include_relationships:
            for name, value in self.__dict__.items():
                if isinstance(value, list):
                    data[name] = [v.to_dict() for v in value if hasattr(v, "to_dict")]
                elif hasattr(value, "to_dict"):
                    data[name] = value.to_dict()
        return data


# ----------------------------------------------------
# Hospital Model
# ----------------------------------------------------
class Hospital(BaseModel, table=True):
    id: Optional[int] = Field(default=1, primary_key=True)
    name: str = Field(default="Default Hospital")
    location: str = Field(default="Default City")

    # Resources
    total_beds: int = Field(default=100)
    available_beds: int = Field(default=100)
    ventilators: int = Field(default=20)
    available_ventilators: int = Field(default=20)
    icu_beds: int = Field(default=10)
    available_icu_beds: int = Field(default=10)
    oxygen_cylinders: int = Field(default=50)
    available_oxygen_cylinders: int = Field(default=50)

    # Relationships
    requests: List["PatientRequest"] = Relationship(back_populates="hospital")
    allocations: List["Allocation"] = Relationship(back_populates="hospital")


# ----------------------------------------------------
# Patient Request Model
# ----------------------------------------------------
class PatientRequest(BaseModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    # Patient info
    name: str
    age: Optional[int] = None
    condition: str

    # Requested resource
    requested_resource: str = Field(default="bed")  # bed | ventilator | icu | oxygen
    status: str = Field(default="waiting")  # waiting | active | discharged

    # Foreign key
    hospital_id: int = Field(default=1, foreign_key="hospital.id")
    hospital: Optional[Hospital] = Relationship(back_populates="requests")

    # Relationship with allocations
    allocations: List["Allocation"] = Relationship(back_populates="patient")


# ----------------------------------------------------
# Allocation Model
# ----------------------------------------------------
class Allocation(BaseModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    # Foreign key to patient
    patient_id: int = Field(foreign_key="patientrequest.id")
    patient: Optional[PatientRequest] = Relationship(
        back_populates="allocations",
        sa_relationship_kwargs={"lazy": "joined"}
    )

    # Allocation details
    resource_type: str  # bed | ventilator | icu | oxygen
    status: str = Field(default="active")
    allocated_at: datetime = Field(default_factory=lambda: datetime.utcnow() + timedelta(hours=5, minutes=30))  # ✅ Changed to IST
    deallocated_at: Optional[datetime] = Field(default=None)

    # Foreign key to hospital
    hospital_id: int = Field(default=1, foreign_key="hospital.id")
    hospital: Optional[Hospital] = Relationship(back_populates="allocations")