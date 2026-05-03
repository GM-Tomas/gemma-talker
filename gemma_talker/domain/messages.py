from dataclasses import dataclass
from typing import Literal


Role = Literal["system", "user", "assistant"]


@dataclass(frozen=True)
class ChatMessage:
    role: Role
    content: str

    def to_dict(self) -> dict[str, str]:
        return {"role": self.role, "content": self.content}

    @classmethod
    def from_dict(cls, raw: dict[str, str]) -> "ChatMessage":
        return cls(role=raw["role"], content=raw["content"])  # type: ignore[arg-type]
