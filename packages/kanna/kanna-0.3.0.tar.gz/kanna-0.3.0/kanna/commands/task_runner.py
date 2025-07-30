import subprocess
import sys

from kanna.renderers import ExecutionRecorder
from kanna.utils import get_command
from kanna.utils.arguments import ArgumentParser
from kanna.utils.project import KannaProject


class TaskRunner:
    def __init__(
        self,
        project: KannaProject,
        argument_parser: ArgumentParser,
        dry_run: bool = False,
        recorder: ExecutionRecorder | None = None,
    ):
        self.project = project
        self.dry_run = dry_run
        self.recorder = recorder
        self._visited: set[str] = set()
        self._argument_parser = argument_parser

    def run(self, task: str) -> set[str]:
        current_command = get_command(identifier=task, project=self.project)

        if current_command is None:
            sys.exit(f"Error: Task '{task}' was not defined.")

        first_run = task not in self._visited
        self._visited.add(task)

        if isinstance(current_command, str):
            self._execute(task, current_command)
            return self._visited

        # 1) Pre-tasks
        self._run_phase(task, current_command.pre, first_run, phase='pre')

        # 2) Main command
        self._execute(task, current_command.command)

        # 3) Post-tasks
        self._run_phase(task, current_command.post, first_run, phase='post')

        return self._visited

    def _run_phase(
        self, parent: str, tasks: list[str], first_run: bool, phase: str
    ) -> None:
        if not tasks:
            return

        if first_run:
            for child in tasks:
                if self.recorder:
                    self.recorder.record_effect(parent, child)
                self.run(child)
        else:
            print(
                f"Info: Skipping {phase}-tasks for '{parent}' "
                f'({tasks}) because it has already been executed.'
            )

    def _execute(self, task: str, command: str) -> None:
        if not command:
            return

        custom_args = self._argument_parser.get_command_custom_args(command)

        if custom_args and not self.dry_run:
            command = self._argument_parser.handle_command_custom_args(
                args=custom_args, command=command
            )

        if self.recorder:
            self.recorder.record_start(task)

        if self.dry_run:
            print(f'[DRY-RUN] Would Execute Task {task}: {command}')
        else:
            subprocess.run(command, shell=True, check=True)
