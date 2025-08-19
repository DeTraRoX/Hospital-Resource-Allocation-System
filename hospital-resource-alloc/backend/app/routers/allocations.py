from fastapi import APIRouter, Depends
from sqlmodel import Session, select
from ..db import get_session
from ..models import Allocation, PatientRequest

router = APIRouter(prefix="/allocations", tags=["Allocations"])

# ✅ Get all active patients for hospital 1
@router.get("/active/1")
def get_active_allocations(session: Session = Depends(get_session)):
    statement = select(Allocation).where(
        Allocation.hospital_id == 1,
        Allocation.status == "active"
    )
    return session.exec(statement).all()

# ✅ Discharge a patient
@router.post("/discharge/{patient_id}")
def discharge_patient(patient_id: int, session: Session = Depends(get_session)):
    # Find allocation
    allocation = session.exec(
        select(Allocation).where(
            Allocation.patient_id == patient_id,
            Allocation.hospital_id == 1,
            Allocation.status == "active"
        )
    ).first()

    if not allocation:
        return {"error": "Patient not found or already discharged"}

    allocation.status = "discharged"
    session.add(allocation)

    # Also update patient request
    patient = session.exec(
        select(PatientRequest).where(
            PatientRequest.id == patient_id,
            PatientRequest.hospital_id == 1
        )
    ).first()

    if patient:
        patient.status = "completed"
        session.add(patient)

    session.commit()
    return {"message": f"Patient {patient_id} discharged"}
