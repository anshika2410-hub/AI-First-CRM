from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from langchain_core.messages import SystemMessage
from app.langgraph_agent import agent
from app.database import Base, engine, get_db
from app.models import Interaction, HCPMaster
from app.schemas import InteractionCreate
from app import crud
from fastapi.middleware.cors import CORSMiddleware
from langchain_core.messages import HumanMessage
from langchain_groq import ChatGroq
from app.config import GROQ_API_KEY
from sqlalchemy import func
from datetime import date
import json 

app = FastAPI(title="AI First CRM")

app.add_middleware(
    
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



Base.metadata.create_all(bind=engine)


@app.get("/")
def home():
    return {
        "message": "AI First CRM Backend Running"
    }


# -----------------------------
# Create Interaction
# -----------------------------

@app.post("/interactions")
def create_interaction(
    interaction: InteractionCreate,
    db: Session = Depends(get_db)
):
    return crud.create_interaction(db, interaction)


# -----------------------------
# Get All Interactions
# -----------------------------

@app.get("/interactions")
def get_interactions(db: Session = Depends(get_db)):
    return crud.get_all_interactions(db)


# -----------------------------
# Get All Doctors
# -----------------------------

@app.get("/hcp")
def get_hcp(db: Session = Depends(get_db)):
    return crud.get_all_hcps(db)

@app.post("/seed")
def seed_database(db: Session = Depends(get_db)):
    return crud.seed_hcp_data(db)
class ChatRequest(BaseModel):
    message: str




@app.post("/chat")
def chat(request: ChatRequest):
    

    message = request.message.lower()

    form_prompt = f"""
Extract interaction details from this sentence.

User message:
{request.message}

Return ONLY JSON:

{{
"hcp_name":"",
"interaction_type":"",
"interaction_date":"",
"interaction_time":"",
"topics":"",
"materials_shared":"",
"samples_distributed":"",
"sentiment":"",
"outcome":"",
"follow_up":""
}}
"""        
    form_response = llm.invoke(form_prompt)
    import json

    form_response = llm.invoke(form_prompt)

    try:
        form_data = json.loads(form_response.content)
    except:
        form_data = {}

    # Force Log Interaction tool
    if (
        message.startswith("log")
        or message.startswith("save")
        or message.startswith("record")
        or "i met" in message
        or "meeting with" in message
    ):
        from app.tools import log_interaction
        response = log_interaction.invoke({"conversation": request.message})
        return {
    "response": f"""✅ **Interaction logged successfully!**

The following details were extracted and added to the form:

• HCP Name: {form_data.get("hcp_name","")}
• Date: {form_data.get("interaction_date","")}
• Time: {form_data.get("interaction_time","")}
• Sentiment: {form_data.get("sentiment","")}
• Outcome: {form_data.get("outcome","")}

Would you like me to suggest follow-up actions or schedule a meeting?""",
    "form_data": form_data
}
    
    # Edit interaction
    if any(word in message for word in ["change", "update", "edit"]):

        from app.tools import edit_interaction

        doctor = "Dr Sharma"

        new_sentiment = None
        new_outcome = None


    # Sentiment extraction

        if "very positive" in message:
            new_sentiment = "very positive"

        elif "positive" in message:
            new_sentiment = "positive"

        elif "negative" in message:
            new_sentiment = "negative"


    # Outcome extraction

        if "doctor agreed" in message:
            new_outcome = "Doctor agreed to prescribe CardioX"

        elif "interested" in message:
            new_outcome = "Interested"


        if new_sentiment is None and new_outcome is None:
            return {
                "response": "I couldn't understand what to edit."
            }


        response = edit_interaction.invoke(
            {
            "doctor_name": doctor,
            "new_sentiment": new_sentiment,
            "new_outcome": new_outcome
            }
        )


        return{

"response":"Interaction extracted successfully.",

"form":{

"hcp_name":"Dr Sharma",

"interaction_type":"Meeting",

"topics":"CardioX",

"sentiment":"Positive",

"follow_up":"Friday"

}

}
    # View History

    if "history" in message or "previous" in message or "show interactions" in message:

        from app.tools import view_interaction_history

        response = view_interaction_history.invoke(
            {
            "doctor_name":"Dr Sharma"
            }
        )

        return {
            "response":response
        }
    
    # Summarize Interactions

    if "summary" in message or "summarize" in message:

        from app.tools import summarize_interactions

        response = summarize_interactions.invoke(
            {
            "doctor_name": "Dr Sharma"
            }
        )

        return {
            "response": response
        }

    # Force Availability tool
    if "available" in message or "availability" in message:
        from app.tools import check_hcp_availability

        import re

        match = re.search(r"Dr\.?\s+[A-Za-z]+", request.message, re.IGNORECASE)

        if match:
            doctor = match.group(0)
        else:
            doctor = "Dr Sharma"

        print("Doctor extracted:", doctor)

        response = check_hcp_availability.invoke({"doctor_name": doctor})
        return {"response": response}

    # Normal LangGraph
    result = agent.invoke(
    {
        "messages": [
            SystemMessage(
                content="""
You are an AI CRM Assistant for pharmaceutical sales representatives.

Rules:
1. Always use the appropriate tool whenever possible.
2. Never make up doctor or interaction information.
3. Always use tool outputs to answer.
4. If the user asks about doctor availability, use check_hcp_availability.
5. If the user wants to log an interaction, use log_interaction.
6. If the user wants to edit an interaction, use edit_interaction.
7. If the user asks to show previous interactions, use view_interaction_history.
8. If the user asks for a summary, use summarize_interactions.
9. Keep responses professional and concise.
"""
            ),
            HumanMessage(content=request.message)
        ]
    }
)

    return {
    "response": result["messages"][-1].content,
    "form_data": form_data
}
llm = ChatGroq(
    model="llama-3.1-8b-instant",
    api_key=GROQ_API_KEY,
    temperature=0
)

class SuggestRequest(BaseModel):
    outcome: str
    sentiment: str
    topics: str
@app.post("/suggest-followup")
def suggest_followup(request: SuggestRequest):

    prompt = f"""
You are a pharmaceutical CRM assistant.

Interaction Details:

Topic: {request.topics}

Sentiment: {request.sentiment}

Outcome: {request.outcome}

Generate exactly 4 follow-up actions.

Do not include Topic, Sentiment, or Outcome.
Do not use markdown bold (**).
Return only simple bullet points.
Each bullet point must be on a new line.

Format:

- Action 1
- Action 2
- Action 3
- Action 4

"""

    response = llm.invoke(prompt)

    return {
        "suggestion": response.content
    }

@app.get("/dashboard")
def dashboard(db: Session = Depends(get_db)):

    total = db.query(Interaction).count()

    positive = db.query(Interaction).filter(
        Interaction.sentiment.ilike("%positive%")
    ).count()

    doctors = db.query(
        func.count(func.distinct(Interaction.hcp_name))
    ).scalar()

    today = db.query(Interaction).filter(
        Interaction.interaction_date == date.today()
    ).count()

    return {
        "total": total,
        "positive": positive,
        "doctors": doctors,
        "today": today
    }