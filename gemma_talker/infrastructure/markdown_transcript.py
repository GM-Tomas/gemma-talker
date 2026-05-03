from datetime import datetime
from pathlib import Path
from typing import Sequence

from gemma_talker.domain.messages import ChatMessage


class MarkdownTranscriptStore:
    def __init__(self, model_name: str, output_dir: Path | None = None) -> None:
        self._model_name = model_name
        self._output_dir = output_dir or Path.cwd()

    def save(
        self,
        history: Sequence[ChatMessage],
        system_prompt: str | None,
        filename: str | Path | None = None,
    ) -> Path:
        now = datetime.now()
        path = Path(filename) if filename else Path(f"chat_{now.strftime('%Y%m%d_%H%M%S')}.md")
        if not path.is_absolute():
            path = self._output_dir / path

        lines = [f"# Chat con {self._model_name}\n_{now.strftime('%d/%m/%Y %H:%M')}_\n\n"]

        if system_prompt:
            lines.append(f"> **System:** {system_prompt}\n\n---\n\n")

        for message in history:
            label = "**Vos**" if message.role == "user" else "**Gemma**"
            lines.append(f"{label}\n\n{message.content}\n\n---\n\n")

        path.write_text("".join(lines), encoding="utf-8")
        return path
