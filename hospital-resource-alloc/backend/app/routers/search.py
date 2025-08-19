from fastapi import APIRouter, Depends
from sqlmodel import select, Session
from ..db import get_session
from ..models import Hospital, PatientRequest  # Correct model name

router = APIRouter(prefix="/search", tags=["Search"])

# Search hospitals by name (case-insensitive)
@router.get("/hospital")
def search_hospital(name: str, session: Session = Depends(get_session)):
    result = session.exec(select(Hospital).where(Hospital.name.ilike(f"%{name}%"))).all()
    return result

# Search patient requests by requested resource
@router.get("/requests")
def search_request(resource: str, session: Session = Depends(get_session)):
    result = session.exec(
        select(PatientRequest).where(PatientRequest.requested_resource.ilike(f"%{resource}%"))
    ).all()
    return result
