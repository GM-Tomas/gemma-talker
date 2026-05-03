#!/usr/bin/env python3
"""Compatibility wrapper for the package entry point.

Prefer running `gemma-talker` after `pip install -e .`, or:

    python -m gemma_talker
"""

from pathlib import Path

from gemma_talker.cli import main
from gemma_talker.config import ChatConfig
from gemma_talker.domain.messages import ChatMessage
from gemma_talker.infrastructure.llama_cpp_model import LlamaCppChatModel
from gemma_talker.infrastructure.markdown_transcript import MarkdownTranscriptStore
from gemma_talker.infrastructure.terminal_ui import HELP_TEXT, TerminalUI


_config = ChatConfig.from_env()
_ui = TerminalUI()

REPO_ID = _config.repo_id
FILENAME = _config.filename
HISTORY_FILE = _config.history_file

llm = None
console = _ui.console


def print_header() -> None:
    _ui.print_header()


def print_user(text: str) -> None:
    _ui.print_user(text)


def stream_response(messages: list[dict[str, str]]) -> str | None:
    if llm is None:
        _ui.print_error("Error al generar respuesta", RuntimeError("Modelo no inicializado"))
        return None

    model = LlamaCppChatModel(
        llm,
        temperature=_config.temperature,
        max_tokens=_config.max_tokens,
    )
    chat_messages = [ChatMessage.from_dict(message) for message in messages]

    try:
        return _ui.render_stream(model.stream_chat(chat_messages))
    except Exception as exc:
        _ui.print_error("Error al generar respuesta", exc)
        return None


def save_conversation(
    history: list[dict[str, str]],
    system_prompt: str | None,
    fname: str | Path | None = None,
) -> str:
    chat_history = [ChatMessage.from_dict(message) for message in history]
    saved_path = MarkdownTranscriptStore(model_name=FILENAME).save(
        chat_history,
        system_prompt,
        fname,
    )
    _ui.print_info(f"Conversacion guardada en {saved_path}")
    return str(saved_path)


if __name__ == "__main__":
    raise SystemExit(main())
