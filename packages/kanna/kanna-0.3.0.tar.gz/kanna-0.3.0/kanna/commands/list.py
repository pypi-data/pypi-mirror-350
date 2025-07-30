from typing import TypedDict, cast

from kanna.utils import KannaProject, get_command


class TaskMap(TypedDict):
    effects: list[str]
    help: str


def _create_task_map(project: KannaProject) -> dict[str, TaskMap]:
    task_map: dict[str, TaskMap] = {}

    for task_name in project.tasks:
        command_data = get_command(identifier=task_name, project=project)

        if command_data is None:
            continue

        if isinstance(command_data, str):
            task_map[task_name] = cast(TaskMap, {})
            continue

        direct_children = set(command_data.pre + command_data.post)

        task_map[task_name] = {
            'effects': list(direct_children),
            'help': command_data.help,
        }

    return task_map


def list_tasks(project: KannaProject):
    task_map = _create_task_map(project=project)

    name_width = max(len('Task'), max(len(task) for task in task_map))
    desc_width = max(
        len('Description'),
        max(len(task_def.get('help', '')) for _, task_def in task_map.items()),
    )
    deps_width = max(
        len('Side-Effects'),
        max(
            len(', '.join(task_def.get('deps', [])))
            for _, task_def in task_map.items()
        ),
    )

    print(
        f'{"Task":<{name_width}}  {"Description":<{desc_width}}  {"Side-Effects":<{deps_width}}'
    )
    print(f'{"-" * name_width}  {"-" * desc_width}  {"-" * deps_width}')

    for task, task_def in task_map.items():
        print(
            f'{task:<{name_width}}  {task_def.get("help", ""):<{desc_width}}  {", ".join(task_def.get("effects", [])):<{deps_width}}'
        )
