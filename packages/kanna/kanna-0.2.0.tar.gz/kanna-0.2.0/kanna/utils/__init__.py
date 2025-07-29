from pathlib import Path
import sys
from typing import TypedDict, cast

import tomli


class CommandConfig(TypedDict):
    command: str
    help: str
    pre: list[str]
    post: list[str]

type Command = str | CommandConfig

class KannaConfig(TypedDict):
    tasks: dict[str, Command]

def load_config_from_project() -> KannaConfig:
    pyproject = Path('pyproject.toml')

    if not pyproject.exists():
        sys.exit("Initialize a pyproject before calling Kanna")
    
    config_data: KannaConfig | None = None

    with pyproject.open('rb') as config:
        config_data = cast(KannaConfig, tomli.load(config).get('tool', {}).get('kanna'))

    return config_data or {}

def get_command(identifier: str, config: KannaConfig) -> Command | None:
    command: Command | None = config.get('tasks', {}).get(identifier)

    if command is None:
        print(f"The {identifier} task was not defined on pyproject")
        return

    return command