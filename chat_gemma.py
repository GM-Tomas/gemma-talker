#!/usr/bin/env python3
import sys
import os
from datetime import datetime
from pathlib import Path

try:
    from huggingface_hub import hf_hub_download
except ImportError:
    print("Faltan dependencias. Ejecutá: pip install huggingface-hub")
    sys.exit(1)

try:
    from llama_cpp import Llama
except ImportError:
    print("Faltan dependencias. Ejecutá: pip install llama-cpp-python")
    sys.exit(1)

try:
    from rich.console import Console
    from rich.panel import Panel
    from rich.markdown import Markdown
    from rich.text import Text
    from rich.live import Live
    from rich.spinner import Spinner
except ImportError:
    print("Faltan dependencias. Ejecutá: pip install rich prompt_toolkit")
    sys.exit(1)

try:
    from prompt_toolkit import PromptSession
    from prompt_toolkit.history import FileHistory
    from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
    from prompt_toolkit.styles import Style as PTStyle
    from prompt_toolkit.formatted_text import HTML
except ImportError:
    print("Faltan dependencias. Ejecutá: pip install rich prompt_toolkit")
    sys.exit(1)

REPO_ID = "bartowski/gemma-2-2b-it-GGUF"
FILENAME = "gemma-2-2b-it-Q4_K_M.gguf"
HISTORY_FILE = Path.home() / ".gemma_chat_history"

llm = None
console = Console()

HELP_TEXT = """\
**Comandos disponibles**

| Comando | Descripción |
|---------|-------------|
| `/help` | Muestra esta ayuda |
| `/clear` | Limpia el historial de conversación |
| `/system <texto>` | Configura o muestra el system prompt |
| `/save` | Guarda la conversación en un archivo .md |
| `/salir` | Sale del chat |

También podés salir con **Ctrl+C** o **Ctrl+D**.
"""

def print_header():
    console.print()
    console.print(
        Panel.fit(
            "[bold cyan]  Gemma 2 (2B)[/bold cyan]  [dim]via llama.cpp[/dim]",
            border_style="cyan",
            padding=(0, 6),
        )
    )
    console.print("[dim]  /help para ver comandos · Ctrl+C para salir[/dim]\n")

def print_user(text: str):
    console.print(
        Panel(
            Text(text, style="bold white"),
            title="[bold blue]Vos[/bold blue]",
            title_align="right",
            border_style="blue",
            padding=(0, 2),
        )
    )

def stream_response(messages: list) -> str | None:
    try:
        stream = llm.create_chat_completion(
            messages=messages,
            stream=True,
            temperature=0.7,
            max_tokens=2048
        )
    except Exception as e:
        console.print(f"\n[bold red]Error al generar respuesta:[/bold red] {e}\n")
        return None

    full = ""

    with Live(console=console, refresh_per_second=20, transient=False) as live:
        live.update(Spinner("dots2", text="[dim] Gemma está pensando...[/dim]"))

        for chunk in stream:
            delta = chunk["choices"][0]["delta"]
            if "content" in delta:
                full += delta["content"]

                if full:
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

def save_conversation(history: list, system_prompt: str | None, fname: str = None):
    if fname is None:
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        fname = f"chat_{ts}.md"
    lines = [f"# Chat con {FILENAME}\n_{datetime.now().strftime('%d/%m/%Y %H:%M')}_\n\n"]

    if system_prompt:
        lines.append(f"> **System:** {system_prompt}\n\n---\n\n")

    for msg in history:
        label = "**Vos**" if msg["role"] == "user" else "**Gemma**"
        lines.append(f"{label}\n\n{msg['content']}\n\n---\n\n")

    Path(fname).write_text("".join(lines), encoding="utf-8")
    console.print(f"[dim]Conversación guardada en [bold]{fname}[/bold][/dim]\n")
    return fname

def main():
    global llm
    print_header()

    console.print(f"[dim]Verificando y cargando el modelo [bold]{FILENAME}[/bold]...[/dim]")
    try:
        with Live(console=console, refresh_per_second=10, transient=True) as live:
            live.update(Spinner("dots", text="[dim] Descargando/Cargando modelo en memoria...[/dim]"))
            model_path = hf_hub_download(repo_id=REPO_ID, filename=FILENAME)
            
            llm = Llama(
                model_path=model_path,
                n_gpu_layers=-1,
                n_ctx=4096,
                verbose=False
            )
        console.print("[dim green]✓ Modelo cargado correctamente.[/dim green]\n")
    except Exception as e:
        console.print(f"\n[bold red]Error al cargar el modelo:[/bold red] {e}\n")
        return

    history: list[dict] = []
    system_prompt: str | None = None

    session = PromptSession(
        history=FileHistory(str(HISTORY_FILE)),
        auto_suggest=AutoSuggestFromHistory(),
        style=PTStyle.from_dict({"": "bold"}),
    )

    while True:
        try:
            raw = session.prompt(HTML("<ansiblue><b>› </b></ansiblue>")).strip()
        except KeyboardInterrupt:
            console.print("\n[dim]Hasta luego.[/dim]")
            break
        except EOFError:
            console.print("\n[dim]Hasta luego.[/dim]")
            break

        if not raw:
            continue

        if raw.startswith("/"):
            parts = raw.split(maxsplit=1)
            cmd = parts[0].lower()
            arg = parts[1] if len(parts) > 1 else ""

            if cmd in ("/salir", "/exit", "/quit"):
                console.print("[dim]Hasta luego.[/dim]")
                break
            elif cmd == "/help":
                console.print(Panel(Markdown(HELP_TEXT), border_style="dim", padding=(1, 2)))
            elif cmd == "/clear":
                history.clear()
                system_prompt = None
                console.clear()
                print_header()
                console.print("[dim]Historial limpiado.[/dim]\n")
            elif cmd == "/save":
                if history:
                    save_conversation(history, system_prompt)
                else:
                    console.print("[dim]No hay conversación para guardar.[/dim]\n")
            elif cmd == "/system":
                if arg:
                    system_prompt = arg
                    console.print(f"[dim]System prompt configurado:[/dim] [italic]{system_prompt}[/italic]\n")
                else:
                    label = f"[italic]{system_prompt}[/italic]" if system_prompt else "[dim](ninguno)[/dim]"
                    console.print(f"System prompt actual: {label}\n")
            else:
                console.print(f"[yellow]Comando desconocido:[/yellow] {cmd} — escribí [bold]/help[/bold]\n")
            continue

        print_user(raw)

        messages: list[dict] = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.extend(history)
        messages.append({"role": "user", "content": raw})

        reply = stream_response(messages)
        if reply:
            history.append({"role": "user", "content": raw})
            history.append({"role": "assistant", "content": reply})

        console.print()

if __name__ == "__main__":
    main()
