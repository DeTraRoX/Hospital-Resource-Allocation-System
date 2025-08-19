from sqlmodel import Session
from app.db import engine
from app.models import Hospital, Request, Allocation

def seed():
    with Session(engine) as session:
        # Create Hospitals
        h1 = Hospital(name="City Hospital", capacity=100)
        h2 = Hospital(name="Green Valley Clinic", capacity=50)
        h3 = Hospital(name="Sunrise Medical Center", capacity=200)

        session.add_all([h1, h2, h3])
        session.commit()
        session.refresh(h1)
        session.refresh(h2)
        session.refresh(h3)

        # Create Requests
        r1 = Request(hospital_id=h1.id, type="Oxygen", quantity=30)
        r2 = Request(hospital_id=h2.id, type="Ventilator", quantity=10)
        r3 = Request(hospital_id=h3.id, type="Beds", quantity=50)

        session.add_all([r1, r2, r3])
        session.commit()
        session.refresh(r1)
        session.refresh(r2)
        session.refresh(r3)

        # Create Allocations
        a1 = Allocation(hospital_id=h1.id, request_id=r1.id, allocated_quantity=20)
        a2 = Allocation(hospital_id=h2.id, request_id=r2.id, allocated_quantity=5)
        a3 = Allocation(hospital_id=h3.id, request_id=r3.id, allocated_quantity=40)

        session.add_all([a1, a2, a3])
        session.commit()

        print("✅ Dummy data added successfully!")

if __name__ == "__main__":
    seed()
