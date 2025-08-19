from fastapi import APIRouter, HTTPException
from sqlmodel import Session, select
from ..db import engine
from ..models import Hospital

router = APIRouter(prefix="/hospitals", tags=["Hospitals"])

@router.post("/", response_model=Hospital)
def create_hospital(hospital: Hospital):
    with Session(engine) as session:
        session.add(hospital)
        session.commit()
        session.refresh(hospital)
        return hospital

@router.get("/", response_model=list[Hospital])
def list_hospitals():
    with Session(engine) as session:
        hospitals = session.exec(select(Hospital)).all()
        return hospitals

@router.get("/{hospital_id}", response_model=Hospital)
def get_hospital(hospital_id: int):
    with Session(engine) as session:
        hospital = session.get(Hospital, hospital_id)
        if not hospital:
            raise HTTPException(status_code=404, detail="Hospital not found")
        return hospital
