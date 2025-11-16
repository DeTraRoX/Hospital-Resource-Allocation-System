from fastapi import APIRouter, Depends
from fastapi.encoders import jsonable_encoder
from sqlmodel import Session, select
from app.db import get_session
from app.models import Allocation, PatientRequest, Hospital
from .ws import broadcast_update, broadcast_waiting_patients, broadcast_active_patients
import asyncio

router = APIRouter(prefix="/allocations", tags=["Allocations"])


# ✅ Helper: Auto-assign next waiting patient
def auto_assign_next(session: Session, hospital: Hospital):
    waiting = session.exec(
        select(PatientRequest).where(
            PatientRequest.hospital_id == 1,
            PatientRequest.status == "waiting"
        )
    ).first()

    if waiting:
        allocation = None

        if waiting.requested_resource == "bed" and hospital.available_beds > 0:
            hospital.available_beds -= 1
            allocation = Allocation(
                hospital_id=1,
                patient_id=waiting.id,
                resource_type="bed",
                status="active"
            )
        elif waiting.requested_resource == "ventilator" and hospital.available_ventilators > 0:
            hospital.available_ventilators -= 1
            allocation = Allocation(
                hospital_id=1,
                patient_id=waiting.id,
                resource_type="ventilator",
                status="active"
            )
        elif waiting.requested_resource == "icu" and hospital.available_icu_beds > 0:
            hospital.available_icu_beds -= 1
            allocation = Allocation(
                hospital_id=1,
                patient_id=waiting.id,
                resource_type="icu",
                status="active"
            )
        elif waiting.requested_resource == "oxygen" and hospital.available_oxygen_cylinders > 0:
            hospital.available_oxygen_cylinders -= 1
            allocation = Allocation(
                hospital_id=1,
                patient_id=waiting.id,
                resource_type="oxygen",
                status="active"
            )

        if allocation:
            # Update patient + save allocation
            waiting.status = "active"
            session.add(allocation)
            session.add(waiting)
            session.add(hospital)
            session.commit()

            # Broadcast updates
            active = session.exec(
                select(Allocation).where(Allocation.hospital_id == 1, Allocation.status == "active")
            ).all()
            waiting_patients = session.exec(
                select(PatientRequest).where(PatientRequest.hospital_id == 1, PatientRequest.status == "waiting")
            ).all()

            # ✅ Use jsonable_encoder to properly serialize datetime objects
            asyncio.create_task(broadcast_active_patients([jsonable_encoder(a) for a in active]))
            asyncio.create_task(broadcast_waiting_patients([jsonable_encoder(p) for p in waiting_patients]))
            asyncio.create_task(broadcast_update({
                "beds": hospital.available_beds,
                "icu": hospital.available_icu_beds,
                "ventilators": hospital.available_ventilators,
                "oxygen": hospital.available_oxygen_cylinders,
            }))


# ✅ Get all active patients for hospital 1
@router.get("/active/1")
def get_active_allocations(session: Session = Depends(get_session)):
    allocations = session.exec(
        select(Allocation).where(
            Allocation.hospital_id == 1,
            Allocation.status == "active"
        )
    ).all()

    # ✅ Manually load patient data for each allocation
    result = []
    for allocation in allocations:
        patient = session.exec(
            select(PatientRequest).where(PatientRequest.id == allocation.patient_id)
        ).first()
        allocation_dict = jsonable_encoder(allocation)
        allocation_dict['patient'] = jsonable_encoder(patient) if patient else None
        result.append(allocation_dict)

    return result


# ✅ Get all allocations (both active and completed) for hospital 1
@router.get("/")
def get_all_allocations(session: Session = Depends(get_session)):
    """Get all allocations including completed ones with deallocated_at timestamp"""
    allocations = session.exec(
        select(Allocation).where(
            Allocation.hospital_id == 1
        ).order_by(Allocation.allocated_at.desc())
    ).all()

    # ✅ Manually load patient data for each allocation
    result = []
    for allocation in allocations:
        patient = session.exec(
            select(PatientRequest).where(PatientRequest.id == allocation.patient_id)
        ).first()
        allocation_dict = jsonable_encoder(allocation)
        allocation_dict['patient'] = jsonable_encoder(patient) if patient else None
        result.append(allocation_dict)

    return result