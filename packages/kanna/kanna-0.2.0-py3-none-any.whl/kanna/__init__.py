import argparse
from pathlib import Path

from kanna.commands.list import list_tasks
from kanna.commands.task_runner import ExecutionRecorder, run_task
from kanna.renderers.dot import DotRenderer
from kanna.renderers.shell import ShellRenderer

from .utils import load_config_from_project


def _add_task_parser(parser: argparse.ArgumentParser):
    parser.add_argument(
        'task', nargs='?', help='Task identifier defined on tool.kanna.tasks'
    )
    parser.add_argument(
        '--plan',
        '-p',
        action='store_true',
        help='Simulate the task execution without making any changes.',
    )
    parser.add_argument(
        '--plan-output-path',
        '-pop',
        help="Plan renderer output path if shell isn't selected",
    )


def _build_argparse() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        'Kanna is a task runner for pyproject environments.'
    )

    _add_task_parser(parser=parser)

    parser.add_argument(
        '--list',
        '-l',
        action='store_true',
        help='List all available tasks that kanna can run',
    )
    return parser.parse_args()


def _plan_execution(
    recorder: ExecutionRecorder, output_path: Path | None = None
) -> None:
    recorder.render(
        output_path=Path(output_path or ''),
        renderer=ShellRenderer() if output_path is None else DotRenderer(),
    )


def run() -> None:
    args = _build_argparse()
    config = load_config_from_project()

    if args.task:
        recorder = ExecutionRecorder()
        run_task(
            task=args.task,
            config=config,
            dry_run=args.plan,
            recorder=recorder,
        )
        if args.plan:
            _plan_execution(
                recorder=recorder, output_path=args.plan_output_path
            )

    elif args.list:
        list_tasks(config=config)
