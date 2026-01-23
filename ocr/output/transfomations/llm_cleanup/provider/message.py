from typing import NamedTuple


class Message(NamedTuple):
    role: str
    content: str
