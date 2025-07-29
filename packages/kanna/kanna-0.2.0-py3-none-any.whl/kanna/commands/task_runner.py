import subprocess
import sys

from kanna.renderers import ExecutionRecorder
from kanna.utils import KannaConfig, get_command


def _execute_command(
    task: str,
    command: str,
    dry_run: bool = False,
    recorder: ExecutionRecorder | None = None,
) -> None:
    if not command or command == '':
        return
    if recorder:
        recorder.record_start(task)
    if dry_run:
        return _execute_dry_run_command(task=task, command=command)
    return _execute_command_on_shell(command=command)


def _execute_command_on_shell(command: str) -> None:
    subprocess.run(command, shell=True, check=True)


def _execute_dry_run_command(task: str, command: str) -> None:
    print(f'[DRY-RUN] Would Execute Task {task}: {command}')


def _execute_nested_tasks(
    parent: str,
    tasks: list[str],
    config: KannaConfig,
    execution_stack: set[str],
    dry_run: bool = False,
    recorder: ExecutionRecorder | None = None,
) -> None:
    for task_name in tasks:
        if recorder:
            recorder.record_effect(parent, task_name)
        run_task(
            task=task_name,
            config=config,
            dry_run=dry_run,
            execution_stack=execution_stack,
            recorder=recorder,
        )


def run_task(
    task: str,
    config: KannaConfig,
    dry_run: bool = False,
    execution_stack: set[str] | None = None,
    recorder: ExecutionRecorder | None = None,
) -> set[str]:
    current_task_local_snapshot_of_stack: set[str] = set()
    execution_stack = execution_stack or set()
    current_task_local_snapshot_of_stack.update(execution_stack)
    execution_stack.add(task)
    already_seen = task not in current_task_local_snapshot_of_stack

    command_details = get_command(identifier=task, config=config)

    if command_details is None:
        sys.exit(f"Error: Task '{task}' was not defined.")

    if isinstance(command_details, str):
        _execute_command(
            task=task,
            command=command_details,
            dry_run=dry_run,
            recorder=recorder,
        )

        return execution_stack

    pre_tasks = command_details.get('pre', [])
    post_tasks = command_details.get('post', [])
    task_main_command = command_details.get('command', '')

    if already_seen:
        _execute_nested_tasks(
            parent=task,
            tasks=pre_tasks,
            config=config,
            execution_stack=execution_stack,
            dry_run=dry_run,
            recorder=recorder,
        )
    elif not already_seen and pre_tasks:
        print(
            f"Info: Skipping pre-tasks for '{task}' "
            "({pre_tasks}) because '{task}' has already been executed "
            'before and it may cause circular dependencies.'
        )

    _execute_command(
        task=task, command=task_main_command, dry_run=dry_run, recorder=recorder
    )

    if already_seen:
        _execute_nested_tasks(
            parent=task,
            tasks=post_tasks,
            config=config,
            execution_stack=execution_stack,
            dry_run=dry_run,
            recorder=recorder,
        )
    elif not already_seen and post_tasks:
        print(
            f"Info: Skipping post-tasks for '{task}' "
            "({post_tasks}) because '{task}' has already been executed "
            'before and it may cause circular dependencies.'
        )

    return execution_stack
