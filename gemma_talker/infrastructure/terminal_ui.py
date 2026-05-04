from contextlib import contextmanager
from pathlib import Path
from typing import Iterable, Iterator

from rich.console import Console
from rich.live import Live
from rich.markdown import Markdown
from rich.panel import Panel
from rich.spinner import Spinner
from rich.text import Text


HELP_TEXT = """\
**Comandos disponibles**

| Comando | Descripcion |
|---------|-------------|
| `/help` | Muestra esta ayuda |
| `/clear` | Limpia el historial de conversacion |
| `/system <texto>` | Configura o muestra el system prompt |
| `/save` | Guarda la conversacion en un archivo .md |
| `/salir` | Sale del chat |

Tambien podes salir con **Ctrl+C** o **Ctrl+D**.
"""


class TerminalUI:
    def __init__(self) -> None:
        self.console = Console()

    @contextmanager
    def spinner(self, text: str, transient: bool = True) -> Iterator[None]:
        with Live(
            Spinner("dots", text=f"[dim] {text}[/dim]"),
            console=self.console,
            refresh_per_second=10,
            transient=transient,
        ):
            yield

    def print_header(self, model_name: str = "Gemma") -> None:
        self.console.print()
        self.console.print(
            Panel.fit(
                f"[bold cyan]  {model_name}[/bold cyan]  [dim]via llama.cpp[/dim]",
                border_style="cyan",
                padding=(0, 6),
            )
        )
        self.console.print("[dim]  /help para ver comandos - Ctrl+C para salir[/dim]\n")

    def print_user(self, text: str) -> None:
        self.console.print(
            Panel(
                Text(text, style="bold white"),
                title="[bold blue]Vos[/bold blue]",
                title_align="right",
                border_style="blue",
                padding=(0, 2),
            )
        )

    def print_help(self) -> None:
        self.console.print(Panel(Markdown(HELP_TEXT), border_style="dim", padding=(1, 2)))

    def print_model_check(self, filename: str) -> None:
        self.console.print(f"[dim]Verificando y cargando el modelo [bold]{filename}[/bold]...[/dim]")

    def print_model_loaded(self) -> None:
        self.console.print("[dim green]OK Modelo cargado correctamente.[/dim green]\n")

    def print_error(self, title: str, error: Exception) -> None:
        self.console.print(f"\n[bold red]{title}:[/bold red] {error}\n")

    def print_info(self, message: str) -> None:
        self.console.print(f"[dim]{message}[/dim]\n")

    def print_warning(self, message: str) -> None:
        self.console.print(f"[yellow]{message}[/yellow]\n")

    def clear(self) -> None:
        self.console.clear()

    def render_stream(self, chunks: Iterable[str]) -> str | None:
        full = ""

        with Live(console=self.console, refresh_per_second=20, transient=False) as live:
            live.update(Spinner("dots2", text="[dim] Gemma esta pensando...[/dim]"))

            for chunk in chunks:
                full += chunk
                live.update(
                    Panel(
                        Text(full),
                        title="[bold green]Gemma[/bold green]",
                        border_style="green",
                        padding=(0, 2),
                    )
                )

            if full:
                live.update(
                    Panel(
                        Markdown(full),
                        title="[bold green]Gemma[/bold green]",
                        border_style="green",
                        padding=(1, 2),
                    )
                )

        return full or None


def create_prompt_session(history_file: Path):
    from prompt_toolkit import PromptSession
    from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
    from prompt_toolkit.history import FileHistory
    from prompt_toolkit.styles import Style as PTStyle

    return PromptSession(
        history=FileHistory(str(history_file)),
        auto_suggest=AutoSuggestFromHistory(),
        style=PTStyle.from_dict({"": "bold"}),
    )


def prompt_marker():
    from prompt_toolkit.formatted_text import HTML

    return HTML("<ansiblue><b>> </b></ansiblue>")
