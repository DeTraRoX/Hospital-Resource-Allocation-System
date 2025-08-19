from fastapi import APIRouter, Depends
from sqlmodel import Session, select
from ..db import get_session
from ..models import Hospital
from .ws import broadcast_update

router = APIRouter(prefix="/hospitals", tags=["Hospital"])

# ✅ Always return hospital 1
@router.get("/")
def get_hospital(session: Session = Depends(get_session)):
    hospital = session.exec(select(Hospital).where(Hospital.id == 1)).first()
    return hospital

# ✅ Update hospital resources & broadcast changes
@router.put("/")
async def update_hospital_resources(updated: Hospital, session: Session = Depends(get_session)):
    hospital = session.exec(select(Hospital).where(Hospital.id == 1)).first()
    if not hospital:
        return {"error": "Hospital not found"}

    # Update values
    hospital.total_beds = updated.total_beds
    hospital.available_beds = updated.available_beds
    hospital.ventilators = updated.ventilators
    hospital.available_ventilators = updated.available_ventilators

    session.add(hospital)
    session.commit()
    session.refresh(hospital)

    # 🔔 Broadcast new summary to all dashboards
    await broadcast_update({
        "total_beds": hospital.total_beds,
        "available_beds": hospital.available_beds,
        "ventilators": hospital.ventilators,
        "available_ventilators": hospital.available_ventilators,
    })

    return {"status": "ok", "hospital": hospital}
