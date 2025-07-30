import re

from kanna.utils.project import KannaProject


class ArgumentParser:
    """
    A simple argument parser that can parse command line arguments.
    """

    def __init__(self, project: KannaProject):
        self._project = project
        self._arg_regex = r'{{kanna:(\w+)}}'

    def get_command_custom_args(self, command: str) -> set[str] | None:
        return set(re.findall(self._arg_regex, command))

    def _ask_user_for_custom_arg(
        self, arg: str
    ) -> dict[str, str | int | float | bool]:
        if arg in self._project.args:
            default_value = self._project.args[arg].default

            if default_value:
                print(f'[ARGUMENT] {arg}: {default_value}')
                return {arg: default_value}

        value = input(f'[ARGUMENT] {arg.capitalize()}: ')
        return {arg: value}

    def _replace_custom_arg_placeholder_with_provided_value(
        self, command: str, arg_mapping: dict[str, str | int | float | bool]
    ) -> str:
        for arg, value in arg_mapping.items():
            placeholder = f'{{{{kanna:{arg}}}}}'
            command = command.replace(placeholder, str(value))
        return command

    def handle_command_custom_args(self, args: set[str], command: str) -> str:
        for arg in args:
            mapping = self._ask_user_for_custom_arg(arg=arg)
            command = self._replace_custom_arg_placeholder_with_provided_value(
                command=command, arg_mapping=mapping
            )
        return command
