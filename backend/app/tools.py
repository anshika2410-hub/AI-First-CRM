from langchain_core.tools import tool
from sqlalchemy.orm import Session
from langchain_groq import ChatGroq
from app.config import GROQ_API_KEY
from app.models import HCPMaster, Interaction
from app.entity_extractor import extract_interaction
llm = ChatGroq(
    model="llama-3.1-8b-instant",
    api_key=GROQ_API_KEY,
    temperature=0
)
@tool
def check_hcp_availability(doctor_name: str):
    """
    Check whether a doctor is available.
    """

    from app.database import SessionLocal

    db: Session = SessionLocal()
    print("Received doctor_name:", repr(doctor_name))
    doctor = (
        db.query(HCPMaster)
        .filter(HCPMaster.doctor_name.ilike(f"%{doctor_name}%"))
        .first()
    )
     # DEBUG
    print("Doctor found:", doctor)
    db.close()

    if doctor:
        return f"""
Doctor Name: {doctor.doctor_name}
Specialty: {doctor.specialty}
Hospital: {doctor.hospital}
City: {doctor.city}
Availability: {doctor.availability}
"""

    return "Doctor not found."

@tool
def log_interaction(conversation: str):
    """
Use this tool whenever the user wants to log, save, record or create an HCP interaction.

Input should be the complete conversation.

This tool extracts structured information using AI and stores it in the CRM database.
"""

    from datetime import date, datetime
    from app.database import SessionLocal

    db = SessionLocal()

    data = extract_interaction(conversation)

    interaction = Interaction(

        hcp_name=data["doctor_name"],

        interaction_type=data["interaction_type"],

        interaction_date=date.today(),

        interaction_time=datetime.now().time(),

        attendees=data["attendees"],

        topics=data["topics"],

        materials_shared=data["materials_shared"],

        samples_distributed=data["samples_distributed"],

        sentiment=data["sentiment"],

        outcome=data["outcome"],

        follow_up=data["follow_up"]

    )

    db.add(interaction)

    db.commit()

    db.close()

    return f"""
Interaction Logged Successfully

Doctor : {data['doctor_name']}
Sentiment : {data['sentiment']}
Outcome : {data['outcome']}
Follow Up : {data['follow_up']}
"""

@tool
def edit_interaction(doctor_name: str, new_sentiment: str = None, new_outcome: str = None):
    """
    Update an existing HCP interaction.

    Use this tool when user wants to change/edit/update an interaction.

    Extract:
    doctor_name = doctor's name

    new_sentiment = updated sentiment value
    Example:
    "very positive", "positive", "negative"

    new_outcome = updated outcome/action/result.
    Example:
    "Doctor agreed to prescribe CardioX"
    """

    from app.database import SessionLocal

    db = SessionLocal()

    interaction = (
        db.query(Interaction)
        .filter(Interaction.hcp_name.ilike(f"%{doctor_name}%"))
        .order_by(Interaction.id.desc())
        .first()
    )

    print("FOUND RECORD ID:", interaction.id)
    print("OLD SENTIMENT:", interaction.sentiment)
    print("OLD OUTCOME:", interaction.outcome)

    if new_sentiment:
        interaction.sentiment = new_sentiment

    if new_outcome:
         interaction.outcome = new_outcome

    print("NEW SENTIMENT:", interaction.sentiment)
    print("NEW OUTCOME:", interaction.outcome)

    db.commit()

    db.refresh(interaction)

    print("AFTER COMMIT SENTIMENT:", interaction.sentiment)
    print("AFTER COMMIT OUTCOME:", interaction.outcome)

    db.close()

    return f"""
    Interaction Updated Successfully

    Doctor : {interaction.hcp_name}

    Sentiment : {interaction.sentiment}

    Outcome : {interaction.outcome}
"""
   
  
@tool
def view_interaction_history(doctor_name: str):
    """
    View all previous interactions of an HCP.
    """

    from app.database import SessionLocal

    db = SessionLocal()

    interactions = (
        db.query(Interaction)
        .filter(Interaction.hcp_name.ilike(f"%{doctor_name}%"))
        .order_by(Interaction.id.desc())
        .all()
    )

    db.close()

    if not interactions:
        return "No interaction history found."

    history = ""

    for i in interactions:

        history += f"""
Doctor : {i.hcp_name}
Date : {i.interaction_date}
Interaction Type : {i.interaction_type}
Topic : {i.topics}
Sentiment : {i.sentiment}
Outcome : {i.outcome}
Follow Up : {i.follow_up}

----------------------------------------
"""

    return history

@tool
def summarize_interactions(doctor_name: str):
    """
    Generate summary of all interactions.
    """

    from app.database import SessionLocal

    db = SessionLocal()

    interactions = (
        db.query(Interaction)
        .filter(Interaction.hcp_name.ilike(f"%{doctor_name}%"))
        .all()
    )

    db.close()

    if not interactions:
        return "No interaction found."

    text = ""

    for i in interactions:

        text += f"""
Topic: {i.topics}

Sentiment: {i.sentiment}

Outcome: {i.outcome}

Follow Up: {i.follow_up}

"""

    summary = llm.invoke(
    f"""
You are an AI CRM assistant for a Pharmaceutical company.

These are Medical Representative (MR) interactions with Healthcare Professional (HCP) {doctor_name}.

Generate a concise professional CRM summary.

Rules:
- Use ONLY the information provided.
- Do NOT invent facts.
- Do NOT mention patient treatment needs.
- Do NOT assume engagement level unless supported by the interaction history.
- If information is missing, state "Not specified".

Include:

1. Overall Engagement
2. Key Discussion Topics
3. Sentiment Trend
4. Outcomes
5. Follow-up Actions
6. Recommendations for Next Visit

Interaction History:

{text}
"""
)

    return summary.content