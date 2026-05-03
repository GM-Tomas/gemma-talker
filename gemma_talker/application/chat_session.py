from dataclasses import dataclass, field
from typing import Iterator

from gemma_talker.application.ports import ChatModel
from gemma_talker.domain.conversation import Conversation


@dataclass
class ChatSession:
    model: ChatModel
    conversation: Conversation = field(default_factory=Conversation)

    def clear(self) -> None:
        self.conversation.clear()

    def set_system_prompt(self, prompt: str | None) -> None:
        self.conversation.set_system_prompt(prompt)

    def stream_reply(self, user_text: str) -> Iterator[str]:
        chunks: list[str] = []
        messages = self.conversation.model_messages_for(user_text)

        for chunk in self.model.stream_chat(messages):
            chunks.append(chunk)
            yield chunk

        reply = "".join(chunks)
        if reply:
            self.conversation.add_exchange(user_text, reply)
