from typing import Sequence

from gemma_talker.application import ChatSession, CommandName, parse_command
from gemma_talker.config import ChatConfig
from gemma_talker.infrastructure.llama_cpp_model import LlamaCppChatModel
from gemma_talker.infrastructure.markdown_transcript import MarkdownTranscriptStore
from gemma_talker.infrastructure.terminal_ui import (
    TerminalUI,
    create_prompt_session,
    prompt_marker,
)


def main(_argv: Sequence[str] | None = None) -> int:
    config = ChatConfig.from_env()
    ui = TerminalUI()
    ui.print_header(config.filename)

    ui.print_model_check(config.filename)
    try:
        with ui.spinner("Descargando/Cargando modelo en memoria..."):
            model = LlamaCppChatModel.from_huggingface(config)
    except Exception as exc:
        ui.print_error("Error al cargar el modelo", exc)
        return 1

    ui.print_model_loaded()
    chat = ChatSession(model=model)
    transcript_store = MarkdownTranscriptStore(model_name=config.filename)
    prompt_session = create_prompt_session(config.history_file)

    while True:
        try:
            raw = prompt_session.prompt(prompt_marker()).strip()
        except KeyboardInterrupt:
            ui.print_info("Hasta luego.")
            return 0
        except EOFError:
            ui.print_info("Hasta luego.")
            return 0

        if not raw:
            continue

        command = parse_command(raw)
        if command:
            if command.name == CommandName.EXIT:
                ui.print_info("Hasta luego.")
                return 0

            if command.name == CommandName.HELP:
                ui.print_help()
                continue

            if command.name == CommandName.CLEAR:
                chat.clear()
                ui.clear()
                ui.print_header()
                ui.print_info("Historial limpiado.")
                continue

            if command.name == CommandName.SAVE:
                history = chat.conversation.transcript_messages()
                if history:
                    saved_path = transcript_store.save(history, chat.conversation.system_prompt)
                    ui.print_info(f"Conversacion guardada en {saved_path}")
                else:
                    ui.print_info("No hay conversacion para guardar.")
                continue

            if command.name == CommandName.SYSTEM:
                if command.argument:
                    chat.set_system_prompt(command.argument)
                    ui.print_info(f"System prompt configurado: {chat.conversation.system_prompt}")
                else:
                    current = chat.conversation.system_prompt or "(ninguno)"
                    ui.print_info(f"System prompt actual: {current}")
                continue

            ui.print_warning(f"Comando desconocido: {command.raw_name}. Escribi /help.")
            continue

        ui.print_user(raw)
        try:
            ui.render_stream(chat.stream_reply(raw))
        except Exception as exc:
            ui.print_error("Error al generar respuesta", exc)

        ui.console.print()

    return 0
