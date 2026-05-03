from dataclasses import dataclass
from typing import Iterable, Sequence

import pytest

from gemma_talker.application.chat_session import ChatSession
from gemma_talker.domain.messages import ChatMessage


@dataclass
class FakeModel:
    chunks: list[str]
    seen_messages: list[ChatMessage] | None = None

    def stream_chat(self, messages: Sequence[ChatMessage]) -> Iterable[str]:
        self.seen_messages = list(messages)
        yield from self.chunks


class BrokenModel:
    def stream_chat(self, messages: Sequence[ChatMessage]) -> Iterable[str]:
        raise RuntimeError("boom")
        yield from ()


def test_stream_reply_yields_chunks_and_commits_history():
    model = FakeModel(["Hola ", "mundo!"])
    session = ChatSession(model=model)

    response = "".join(session.stream_reply("Hola"))

    assert response == "Hola mundo!"
    assert model.seen_messages == [ChatMessage("user", "Hola")]
    assert session.conversation.history == [
        ChatMessage("user", "Hola"),
        ChatMessage("assistant", "Hola mundo!"),
    ]


def test_stream_reply_includes_system_prompt_and_previous_history():
    model = FakeModel(["Listo"])
    session = ChatSession(model=model)
    session.set_system_prompt("Sos breve.")
    session.conversation.add_exchange("Uno", "Dos")

    assert "".join(session.stream_reply("Tres")) == "Listo"

    assert model.seen_messages == [
        ChatMessage("system", "Sos breve."),
        ChatMessage("user", "Uno"),
        ChatMessage("assistant", "Dos"),
        ChatMessage("user", "Tres"),
    ]


def test_stream_reply_does_not_commit_failed_generation():
    session = ChatSession(model=BrokenModel())

    with pytest.raises(RuntimeError):
        list(session.stream_reply("Hola"))

    assert session.conversation.history == []
