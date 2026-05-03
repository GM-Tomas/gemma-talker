from dataclasses import dataclass
from enum import Enum


class CommandName(str, Enum):
    HELP = "help"
    CLEAR = "clear"
    SYSTEM = "system"
    SAVE = "save"
    EXIT = "exit"
    UNKNOWN = "unknown"


@dataclass(frozen=True)
class Command:
    name: CommandName
    argument: str = ""
    raw_name: str = ""


EXIT_ALIASES = {"/salir", "/exit", "/quit"}


def parse_command(raw: str) -> Command | None:
    if not raw.startswith("/"):
        return None

    parts = raw.split(maxsplit=1)
    raw_name = parts[0].lower()
    argument = parts[1] if len(parts) > 1 else ""

    if raw_name in EXIT_ALIASES:
        return Command(CommandName.EXIT, argument, raw_name)
    if raw_name == "/help":
        return Command(CommandName.HELP, argument, raw_name)
    if raw_name == "/clear":
        return Command(CommandName.CLEAR, argument, raw_name)
    if raw_name == "/save":
        return Command(CommandName.SAVE, argument, raw_name)
    if raw_name == "/system":
        return Command(CommandName.SYSTEM, argument, raw_name)

    return Command(CommandName.UNKNOWN, argument, raw_name)
