from dataclasses import dataclass, field
from typing import Sequence

from gemma_talker.domain.messages import ChatMessage


@dataclass
class Conversation:
    history: list[ChatMessage] = field(default_factory=list)
    system_prompt: str | None = None

    def clear(self) -> None:
        self.history.clear()
        self.system_prompt = None

    def set_system_prompt(self, prompt: str | None) -> None:
        self.system_prompt = prompt.strip() if prompt else None

    def model_messages_for(self, user_text: str) -> list[ChatMessage]:
        messages: list[ChatMessage] = []
        if self.system_prompt:
            messages.append(ChatMessage("system", self.system_prompt))
        messages.extend(self.history)
        messages.append(ChatMessage("user", user_text))
        return messages

    def add_exchange(self, user_text: str, assistant_text: str) -> None:
        self.history.append(ChatMessage("user", user_text))
        self.history.append(ChatMessage("assistant", assistant_text))

    def transcript_messages(self) -> Sequence[ChatMessage]:
        return tuple(self.history)
