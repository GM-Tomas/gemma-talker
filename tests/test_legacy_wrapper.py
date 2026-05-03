from unittest.mock import MagicMock

import chat_gemma


def test_legacy_save_conversation(tmp_path):
    saved_path = chat_gemma.save_conversation(
        [
            {"role": "user", "content": "Hola Gemma"},
            {"role": "assistant", "content": "Hola!"},
        ],
        system_prompt="Sos util.",
        fname=tmp_path / "chat.md",
    )

    assert saved_path == str(tmp_path / "chat.md")
    assert "Hola Gemma" in (tmp_path / "chat.md").read_text(encoding="utf-8")


def test_legacy_stream_response_success():
    chat_gemma.llm = MagicMock()
    chat_gemma.llm.create_chat_completion.return_value = iter(
        [
            {"choices": [{"delta": {"content": "Hola "}}]},
            {"choices": [{"delta": {"content": "mundo!"}}]},
        ]
    )

    response = chat_gemma.stream_response([{"role": "user", "content": "Hola"}])

    assert response == "Hola mundo!"


def test_legacy_stream_response_error():
    chat_gemma.llm = MagicMock()
    chat_gemma.llm.create_chat_completion.side_effect = RuntimeError("boom")

    assert chat_gemma.stream_response([{"role": "user", "content": "Hola"}]) is None
