# Agent State Management Logic
from typing import TypedDict

class AgentState(TypedDict):
    messages: list
    current_step: str
