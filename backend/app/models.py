from sqlalchemy import Column, Integer, String, Text, Date, Time

from app.database import Base


class Interaction(Base):

    __tablename__ = "interactions"

    id = Column(Integer, primary_key=True, index=True)

    hcp_name = Column(String(200))

    interaction_type = Column(String(100))

    interaction_date = Column(Date)

    interaction_time = Column(Time)

    attendees = Column(Text)

    topics = Column(Text)

    materials_shared = Column(Text)

    samples_distributed = Column(Text)

    sentiment = Column(String(100))

    outcome = Column(Text)

    follow_up = Column(Text)

class HCPMaster(Base):

    __tablename__ = "hcp_master"

    id = Column(Integer, primary_key=True, index=True)

    doctor_name = Column(String(200), unique=True)

    specialty = Column(String(150))

    hospital = Column(String(200))

    city = Column(String(100))

    availability = Column(String(100))