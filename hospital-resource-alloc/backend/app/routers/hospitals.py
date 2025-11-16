from fastapi import APIRouter, Depends
from sqlmodel import select, Session
from pydantic import BaseModel
from app.db import get_session
from app.models import Hospital
from .ws import broadcast_update

router = APIRouter(prefix="/hospitals", tags=["Hospital"])


# ✅ Schema for partial hospital updates
class HospitalUpdate(BaseModel):
    total_beds: int | None = None
    available_beds: int | None = None
    ventilators: int | None = None
    available_ventilators: int | None = None


# ✅ Always return hospital 1
@router.get("/")
def get_hospital(session: Session = Depends(get_session)):
    hospital = session.exec(select(Hospital).where(Hospital.id == 1)).first()
    return hospital


# ✅ Update hospital resources & broadcast changes
@router.put("/")
async def update_hospital_resources(updated: HospitalUpdate, session: Session = Depends(get_session)):
    hospital = session.exec(select(Hospital).where(Hospital.id == 1)).first()
    if not hospital:
        return {"error": "Hospital not found"}

    # Update only provided fields
    if updated.total_beds is not None:
        hospital.total_beds = updated.total_beds
    if updated.available_beds is not None:
        hospital.available_beds = updated.available_beds
    if updated.ventilators is not None:
        hospital.ventilators = updated.ventilators
    if updated.available_ventilators is not None:
        hospital.available_ventilators = updated.available_ventilators

    session.add(hospital)
    session.commit()
    session.refresh(hospital)

    # 🔔 Broadcast new summary to all dashboards
    await broadcast_update(hospital.model_dump())

    return {"status": "ok", "hospital": hospital.model_dump()}
