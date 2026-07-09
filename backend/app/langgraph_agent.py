from langchain_groq import ChatGroq
from langgraph.prebuilt import create_react_agent
from langchain_core.messages import SystemMessage
from app.tools import view_interaction_history
from app.tools import summarize_interactions
from app.tools import (
    check_hcp_availability,
    log_interaction,
    edit_interaction
)
from app.config import GROQ_API_KEY

llm = ChatGroq(
    model="llama-3.1-8b-instant",
    api_key=GROQ_API_KEY,
    temperature=0
)

system_prompt = SystemMessage(
    content="""
You are an AI CRM assistant for pharmaceutical sales representatives.

IMPORTANT RULES:

1. If the user wants to LOG, SAVE, RECORD or CREATE an interaction,
ALWAYS use the log_interaction tool.

Examples:
- Log this interaction...
- Save today's meeting...
- Record meeting...
- I met Dr Sharma today...
- Doctor gave positive feedback...
- We discussed CardioX...

2. If the user asks:
- Is Dr Sharma available?
- Doctor availability
- Hospital details
- Which city is Dr Sharma in?

ALWAYS use check_hcp_availability tool.

Never answer from your own knowledge if a tool exists.
Always call the correct tool.
"""
)

agent = create_react_agent(
    llm,
    tools=[
        check_hcp_availability,
        log_interaction,
        edit_interaction,
        view_interaction_history,
        summarize_interactions
    ],
    prompt=system_prompt
)