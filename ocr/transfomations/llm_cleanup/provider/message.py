from typing import NamedTuple


class Message(NamedTuple):
    role: str
    content: str

    def as_dict(self) -> dict[str, str]:
        return self._asdict()
