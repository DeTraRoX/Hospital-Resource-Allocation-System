from fastapi import APIRouter, Depends
from sqlmodel import Session, select
from ..db import get_session
from ..models import PatientRequest

router = APIRouter(prefix="/requests", tags=["Requests"])

# ✅ Create a new patient request
@router.post("/")
def create_request(request: dict, session: Session = Depends(get_session)):
    new_request = PatientRequest(
        hospital_id=1,  # Always hospital 1
        condition=request["condition"],
        requested_resource=request.get("requested_resource", "bed"),  # fallback
        status="waiting"
    )
    session.add(new_request)
    session.commit()
    session.refresh(new_request)
    return new_request

# ✅ Get all waiting patients for hospital 1
@router.get("/waiting/1")
def get_waiting_patients(session: Session = Depends(get_session)):
    statement = select(PatientRequest).where(
        PatientRequest.hospital_id == 1,
        PatientRequest.status == "waiting"
    )
    return session.exec(statement).all()
