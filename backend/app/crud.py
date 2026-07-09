from sqlalchemy.orm import Session
from app.models import Interaction, HCPMaster
from app.schemas import InteractionCreate


# -------------------------------
# Interaction CRUD
# -------------------------------

def create_interaction(db: Session, interaction: InteractionCreate):
    new_interaction = Interaction(
        hcp_name=interaction.hcp_name,
        interaction_type=interaction.interaction_type,
        interaction_date=interaction.interaction_date,
        interaction_time=interaction.interaction_time,
        attendees=interaction.attendees,
        topics=interaction.topics,
        materials_shared=interaction.materials_shared,
        samples_distributed=interaction.samples_distributed,
        sentiment=interaction.sentiment,
        outcome=interaction.outcome,
        follow_up=interaction.follow_up
    )

    db.add(new_interaction)
    db.commit()
    db.refresh(new_interaction)

    return new_interaction


def get_all_interactions(db: Session):
    return db.query(Interaction).all()


# -------------------------------
# HCP CRUD
# -------------------------------

def get_hcp_by_name(db: Session, doctor_name: str):
    return (
        db.query(HCPMaster)
        .filter(HCPMaster.doctor_name == doctor_name)
        .first()
    )


def get_all_hcps(db: Session):
    return db.query(HCPMaster).all()

def seed_hcp_data(db: Session):

    existing = db.query(HCPMaster).first()

    if existing:
        return {"message": "HCP data already exists"}

    doctors = [

        HCPMaster(
            doctor_name="Dr Sharma",
            specialty="Cardiologist",
            hospital="Apollo Hospital",
            city="Delhi",
            availability="Available Tomorrow"
        ),

        HCPMaster(
            doctor_name="Dr Mehta",
            specialty="Oncologist",
            hospital="Fortis Hospital",
            city="Jaipur",
            availability="Busy Today"
        ),

        HCPMaster(
            doctor_name="Dr Singh",
            specialty="Neurologist",
            hospital="Max Hospital",
            city="Noida",
            availability="Available Today"
        ),

        HCPMaster(
            doctor_name="Dr Verma",
            specialty="Dermatologist",
            hospital="Medanta",
            city="Gurgaon",
            availability="On Leave"
        )

    ]

    db.add_all(doctors)

    db.commit()

    return {"message": "Sample doctors inserted successfully"}