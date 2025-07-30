from kanna.utils.project import Command, KannaProject


def get_command(identifier: str, project: KannaProject) -> Command | None:
    command: Command | None = project.tasks.get(identifier)

    if command is None:
        print(f'The {identifier} task was not defined on pyproject')
        return

    return command
