from dataclasses import dataclass
from typing import Optional, Any

@dataclass
class Message:
    message_id: int
    chat: dict
    date: int
    text: Optional[str] = None
    photo: Optional[list] = None
    video: Optional[dict] = None
    audio: Optional[dict] = None
    document: Optional[dict] = None
    sticker: Optional[dict] = None
    voice: Optional[dict] = None
    caption: Optional[str] = None
    from_user: Optional[dict] = None

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)