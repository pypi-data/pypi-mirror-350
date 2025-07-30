from typing import Optional
from typing import TypedDict


class Message(TypedDict):
    content: str
    role: str
    timestamp: Optional[str]
