from pathlib import Path

from gemma_talker.domain.messages import ChatMessage
from gemma_talker.infrastructure.llama_cpp_model import LlamaCppChatModel
from gemma_talker.infrastructure.markdown_transcript import MarkdownTranscriptStore


class FakeLlama:
    def __init__(self) -> None:
        self.request = None

    def create_chat_completion(self, **kwargs):
        self.request = kwargs
        return iter(
            [
                {"choices": [{"delta": {"content": "Hola "}}]},
                {"choices": [{"delta": {}}]},
                {"choices": [{"delta": {"content": "mundo!"}}]},
            ]
        )


def test_llama_cpp_chat_model_streams_content_chunks():
    llama = FakeLlama()
    model = LlamaCppChatModel(llama, temperature=0.3, max_tokens=123)

    chunks = list(model.stream_chat([ChatMessage("user", "Hola")]))

    assert chunks == ["Hola ", "mundo!"]
    assert llama.request == {
        "messages": [{"role": "user", "content": "Hola"}],
        "stream": True,
        "temperature": 0.3,
        "max_tokens": 123,
    }


def test_markdown_transcript_store_saves_conversation(tmp_path: Path):
    store = MarkdownTranscriptStore("gemma-test.gguf", output_dir=tmp_path)

    saved_path = store.save(
        [
            ChatMessage("user", "Hola Gemma"),
            ChatMessage("assistant", "Hola! Como puedo ayudarte hoy?"),
        ],
        system_prompt="Sos util.",
        filename="chat.md",
    )

    content = saved_path.read_text(encoding="utf-8")
    assert saved_path == tmp_path / "chat.md"
    assert "# Chat con gemma-test.gguf" in content
    assert "> **System:** Sos util." in content
    assert "**Vos**\n\nHola Gemma" in content
    assert "**Gemma**\n\nHola! Como puedo ayudarte hoy?" in content
