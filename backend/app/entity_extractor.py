import json
import re
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage
from app.config import GROQ_API_KEY

llm = ChatGroq(
    model="llama-3.1-8b-instant",
    api_key=GROQ_API_KEY,
    temperature=0
)


def extract_interaction(conversation: str):

    prompt = f"""
You are an AI CRM assistant.

Extract the following information from the conversation.

Return ONLY a valid JSON object. Do not use markdown. Do not use ```json.

Fields:
doctor_name
interaction_type
attendees
topics
materials_shared
samples_distributed
sentiment
outcome
follow_up

If a field is missing, return an empty string ""

Outcome should be a complete professional sentence.

Examples:
- Doctor agreed to prescribe CardioX.
- Doctor requested additional clinical evidence.
- Follow-up meeting scheduled.
- No commitment from doctor.

Interaction Type must be one of:
- Meeting
- Phone Call
- Virtual Meeting
- Email
- Conference
- Follow-up Visit

Do not return "Log interaction".

Conversation:
{conversation}
"""

    response = llm.invoke([HumanMessage(content=prompt)])

    print("LLM RESPONSE:")
    print(response.content)

    text = response.content.strip()

    # Extract JSON even if wrapped in ```json ... ```
    match = re.search(r"\{.*\}", text, re.DOTALL)

    if not match:
        raise Exception(f"Could not parse JSON.\nLLM Response:\n{text}")

    data = json.loads(match.group())

    return data