from pathlib import Path
from typing import Iterable, Protocol, Sequence

from gemma_talker.domain.messages import ChatMessage


class ChatModel(Protocol):
    def stream_chat(self, messages: Sequence[ChatMessage]) -> Iterable[str]:
        """Yield response chunks for a chat completion."""


class TranscriptStore(Protocol):
    def save(
        self,
        history: Sequence[ChatMessage],
        system_prompt: str | None,
        filename: str | Path | None = None,
    ) -> Path:
        """Persist a conversation transcript and return its path."""
