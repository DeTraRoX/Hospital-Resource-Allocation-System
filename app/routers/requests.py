# backend/app/routers/requests.py
from fastapi.encoders import jsonable_encoder
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from app.db import get_session
from app.models import PatientRequest, Allocation, Hospital
from .ws import broadcast_update, broadcast_waiting_patients, broadcast_active_patients
from datetime import datetime, timezone, timedelta  # ✅ Updated import
import asyncio

router = APIRouter(prefix="/requests", tags=["Requests"])

# ✅ Define IST timezone
IST = timezone(timedelta(hours=5, minutes=30))

# Priority mapping for auto-promotion
PRIORITY_ORDER = {
    "critical": 1,
    "serious": 2,
    "normal": 3
}


# ✅ Create new patient request
@router.post("/")
async def create_request(request: PatientRequest, session: Session = Depends(get_session)):
    try:
        hospital = session.exec(select(Hospital).where(Hospital.id == 1)).first()

        if not hospital:
            raise HTTPException(status_code=404, detail="Hospital not found")

        request.hospital_id = 1
        request.status = "waiting"

        # ✅ Try to allocate resource if available
        is_allocated = False
        if request.requested_resource == "bed" and hospital.available_beds > 0:
            hospital.available_beds -= 1
            is_allocated = True
        elif request.requested_resource == "ventilator" and hospital.available_ventilators > 0:
            hospital.available_ventilators -= 1
            is_allocated = True
        elif request.requested_resource == "icu" and hospital.available_icu_beds > 0:
            hospital.available_icu_beds -= 1
            is_allocated = True
        elif request.requested_resource == "oxygen" and hospital.available_oxygen_cylinders > 0:
            hospital.available_oxygen_cylinders -= 1
            is_allocated = True

        if is_allocated:
            request.status = "active"

        session.add(request)
        session.commit()
        session.refresh(request)

        # Create allocation if active
        if request.status == "active":
            allocation = Allocation(
                hospital_id=1,
                patient_id=request.id,
                resource_type=request.requested_resource,
                status="active"
            )
            session.add(allocation)

        session.add(hospital)
        session.commit()

        active = session.exec(
            select(Allocation).where(Allocation.hospital_id == 1, Allocation.status == "active")
        ).all()
        waiting_patients = session.exec(
            select(PatientRequest).where(PatientRequest.hospital_id == 1, PatientRequest.status == "waiting")
        ).all()

        await broadcast_active_patients([jsonable_encoder(a) for a in active])
        await broadcast_waiting_patients([jsonable_encoder(p) for p in waiting_patients])
        await broadcast_update({
            "beds": hospital.available_beds,
            "icu": hospital.available_icu_beds,
            "ventilators": hospital.available_ventilators,
            "oxygen": hospital.available_oxygen_cylinders,
        })

        return {
            "message": "Request received",
            "status": request.status,
            "patient": jsonable_encoder(request)
        }
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=str(e))


# ✅ Discharge patient + Auto-Promotion
@router.post("/discharge/{request_id}")
async def discharge_patient(request_id: int, session: Session = Depends(get_session)):
    try:
        allocation = session.exec(
            select(Allocation).where(Allocation.patient_id == request_id, Allocation.status == "active")
        ).first()

        if not allocation:
            raise HTTPException(status_code=404, detail="Active allocation not found for this patient")

        hospital = session.exec(select(Hospital).where(Hospital.id == allocation.hospital_id)).first()
        if not hospital:
            raise HTTPException(status_code=404, detail="Hospital not found")

        # Free the allocated resource
        if allocation.resource_type == "bed":
            hospital.available_beds += 1
        elif allocation.resource_type == "ventilator":
            hospital.available_ventilators += 1
        elif allocation.resource_type == "icu":
            hospital.available_icu_beds += 1
        elif allocation.resource_type == "oxygen":
            hospital.available_oxygen_cylinders += 1

        # ✅ Mark allocation as completed with IST timestamp
        allocation.status = "completed"
        allocation.deallocated_at = datetime.utcnow() + timedelta(hours=5, minutes=30) # ✅ Changed to IST

        request = session.exec(select(PatientRequest).where(PatientRequest.id == request_id)).first()
        if request:
            request.status = "completed"

        session.add_all([hospital, allocation, request])
        session.commit()

        # ✅ Auto-Promotion Logic with Priority
        waiting_requests = session.exec(
            select(PatientRequest)
            .where(
                PatientRequest.hospital_id == hospital.id,
                PatientRequest.status == "waiting",
                PatientRequest.requested_resource == allocation.resource_type
            )
        ).all()

        # Sort by priority first (critical > serious > normal), then FIFO
        waiting_requests = sorted(
            waiting_requests,
            key=lambda r: (PRIORITY_ORDER.get(r.condition, 3), r.id)
        )

        promoted_request = None
        if waiting_requests:
            promoted_request = waiting_requests[0]

            # Allocate the freed resource to this patient
            if allocation.resource_type == "bed":
                hospital.available_beds -= 1
            elif allocation.resource_type == "ventilator":
                hospital.available_ventilators -= 1
            elif allocation.resource_type == "icu":
                hospital.available_icu_beds -= 1
            elif allocation.resource_type == "oxygen":
                hospital.available_oxygen_cylinders -= 1

            promoted_request.status = "active"
            new_allocation = Allocation(
                hospital_id=hospital.id,
                patient_id=promoted_request.id,
                resource_type=promoted_request.requested_resource,
                status="active"
            )

            session.add_all([hospital, promoted_request, new_allocation])
            session.commit()

        active = session.exec(
            select(Allocation).where(Allocation.hospital_id == hospital.id, Allocation.status == "active")
        ).all()
        waiting_patients = session.exec(
            select(PatientRequest).where(PatientRequest.hospital_id == hospital.id, PatientRequest.status == "waiting")
        ).all()

        await broadcast_active_patients([jsonable_encoder(a) for a in active])
        await broadcast_waiting_patients([jsonable_encoder(p) for p in waiting_patients])
        await broadcast_update({
            "beds": hospital.available_beds,
            "icu": hospital.available_icu_beds,
            "ventilators": hospital.available_ventilators,
            "oxygen": hospital.available_oxygen_cylinders,
        })

        return {
            "message": "Patient discharged. Resource freed.",
            "auto_promoted": jsonable_encoder(promoted_request) if promoted_request else None
        }
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=str(e))


# ✅ New Endpoint to get all waiting patients
@router.get("/waiting/1")
def get_waiting_requests(session: Session = Depends(get_session)):
    waiting_requests = session.exec(
        select(PatientRequest).where(
            PatientRequest.hospital_id == 1,
            PatientRequest.status == "waiting"
        )
    ).all()
    return waiting_requests