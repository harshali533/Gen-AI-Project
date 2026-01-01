# agent_router.py

from chatbot import get_answer
from tools.location_tool import LocationTool
from tools.contact_tool import ContactTool

class AgentRouter:
    def __init__(self):
        self.location_tool = LocationTool()
        self.contact_tool = ContactTool()

    def route(self, query: str) -> str:
        q = query.lower()

        if "location" in q or "address" in q or "map" in q:
            return self.location_tool.run()

        if "contact" in q or "phone" in q or "email" in q:
            return self.contact_tool.run()

        # fallback → RAG
        return get_answer(query)


# ✅ VERY IMPORTANT: function wrapper
_agent = AgentRouter()

def agent_router(query: str) -> str:
    """
    Wrapper function for UI / Streamlit
    """
    return _agent.route(query)
