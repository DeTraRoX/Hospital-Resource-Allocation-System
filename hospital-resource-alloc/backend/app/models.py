from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import datetime
from pydantic import validator


# ----------------------------------------------------
# Base mixin for dict conversion
# ----------------------------------------------------
class BaseModel(SQLModel):
    class Config:
        orm_mode = True
        json_encoders = {
            datetime: lambda v: v.isoformat() if v else None
        }

    def to_dict(self, include_relationships: bool = False):
        data = self.dict()
        if include_relationships:
            for name, value in self.__dict__.items():
                if isinstance(value, list):
                    data[name] = [v.to_dict() for v in value if hasattr(v, "to_dict")]
                elif hasattr(value, "to_dict"):
                    data[name] = value.to_dict()
        return data

    def model_dump(self, **kwargs):
        """Override model_dump to handle datetime serialization"""
        data = super().model_dump(**kwargs)
        for key, value in data.items():
            if isinstance(value, datetime):
                data[key] = value.isoformat()
        return data


# ----------------------------------------------------
# Hospital Model
# ----------------------------------------------------
class Hospital(BaseModel, table=True):
    id: Optional[int] = Field(default=1, primary_key=True)
    name: str = Field(default="Default Hospital")
    location: str = Field(default="Default City")

    # Resources - All set to 5
    total_beds: int = Field(default=5)
    available_beds: int = Field(default=5)
    ventilators: int = Field(default=5)
    available_ventilators: int = Field(default=5)
    icu_beds: int = Field(default=5)
    available_icu_beds: int = Field(default=5)
    oxygen_cylinders: int = Field(default=5)
    available_oxygen_cylinders: int = Field(default=5)

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
    patient: Optional[PatientRequest] = Relationship(back_populates="allocations")

    # Allocation details
    resource_type: str  # bed | ventilator | icu | oxygen
    status: str = Field(default="active")
    allocated_at: datetime = Field(default_factory=datetime.utcnow)

    # Foreign key to hospital
    hospital_id: int = Field(default=1, foreign_key="hospital.id")
    hospital: Optional[Hospital] = Relationship(back_populates="allocations")

    def model_dump(self, **kwargs):
        """Override model_dump to handle datetime serialization"""
        data = super().model_dump(**kwargs)
        if 'allocated_at' in data and isinstance(data['allocated_at'], datetime):
            data['allocated_at'] = data['allocated_at'].isoformat()
        return data