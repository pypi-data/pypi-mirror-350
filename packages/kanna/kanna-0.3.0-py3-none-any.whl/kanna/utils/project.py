import sys
from dataclasses import dataclass
from pathlib import Path
from typing import TypedDict

import tomli

type Command = str | CommandConfig
type ICommand = str | ICommandConfig
type IKannaTasks = dict[str, ICommand]
type IKannaArgs = dict[str, IKannaArg]


class ICommandConfig(TypedDict):
    command: str
    help: str
    pre: list[str]
    post: list[str]


class IKannaArg(TypedDict):
    default: str | int | float | bool
    help: str


class IKannaTools(TypedDict):
    tasks: IKannaTasks
    args: IKannaArgs


@dataclass
class CommandConfig:
    command: str
    help: str
    pre: list[str]
    post: list[str]


@dataclass
class Argument:
    default: str | int | float | bool
    help: str


type KannaTasks = dict[str, Command]
type KannaArgs = dict[str, Argument]


@dataclass
class KannaProject:
    tasks: KannaTasks
    args: KannaArgs

    @staticmethod
    def _get_commands_from_pyproject(tasks: IKannaTasks) -> KannaTasks:
        normalized_tasks: KannaTasks = {}

        for task, command in tasks.items():
            if isinstance(command, str):
                tasks[task] = command
                continue

            normalized_tasks[task] = CommandConfig(
                command=command.get('command'),
                help=command.get('help', ''),
                pre=command.get('pre', []),
                post=command.get('post', []),
            )

        return normalized_tasks

    @staticmethod
    def _get_args_from_pyproject(args: IKannaArgs) -> KannaArgs:
        normalized_args: KannaArgs = {}

        for arg, value in args.items():
            normalized_args[arg] = Argument(
                default=value.get('default', ''),
                help=value.get('help', ''),
            )

        return normalized_args

    @staticmethod
    def from_pyproject() -> 'KannaProject':
        pyproject = Path('pyproject.toml')

        if not pyproject.exists():
            sys.exit(
                'Initialize a pyproject before calling Kanna'
            )  # TODO: add better error raising

        kanna_tools: IKannaTools | None = None

        with pyproject.open('rb') as config:
            kanna_tools = tomli.load(config).get('tool', {}).get('kanna')

        if kanna_tools is None:
            raise Exception(
                'Kanna tools not found in pyproject.toml. '
                'Please add a [tool.kanna] section.'
            )

        tasks = KannaProject._get_commands_from_pyproject(
            tasks=kanna_tools.get('tasks', {})
        )
        args = KannaProject._get_args_from_pyproject(
            args=kanna_tools.get('args', {})
        )

        return KannaProject(tasks=tasks, args=args)
