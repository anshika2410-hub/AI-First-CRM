from pydantic import BaseModel
from datetime import date, time


class InteractionCreate(BaseModel):

    hcp_name: str

    interaction_type: str

    interaction_date: date

    interaction_time: time

    attendees: str

    topics: str

    materials_shared: str

    samples_distributed: str

    sentiment: str

    outcome: str

    follow_up: str


class InteractionResponse(InteractionCreate):

    id: int

    class Config:
        from_attributes = True

class HCPCreate(BaseModel):

    doctor_name: str
    specialty: str
    hospital: str
    city: str
    availability: str


class HCPResponse(HCPCreate):

    id: int

    class Config:
        from_attributes = True