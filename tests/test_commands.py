from gemma_talker.application.commands import CommandName, parse_command


def test_parse_command_returns_none_for_regular_text():
    assert parse_command("hola") is None


def test_parse_known_commands():
    assert parse_command("/help").name == CommandName.HELP
    assert parse_command("/clear").name == CommandName.CLEAR
    assert parse_command("/save").name == CommandName.SAVE
    assert parse_command("/salir").name == CommandName.EXIT


def test_parse_system_command_argument():
    command = parse_command("/system Sos una asistente util")

    assert command.name == CommandName.SYSTEM
    assert command.argument == "Sos una asistente util"


def test_parse_unknown_command_keeps_raw_name():
    command = parse_command("/nope algo")

    assert command.name == CommandName.UNKNOWN
    assert command.raw_name == "/nope"
    assert command.argument == "algo"
