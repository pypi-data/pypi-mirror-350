import sys
from pathlib import Path

from kanna.renderers.dot import DotRenderer
from kanna.renderers.shell import ShellRenderer


class ExecutionRecorder:
    def __init__(
        self,
    ):
        self._sequence: list[str] = []
        self._edges: set[tuple[str, str]] = set()

    def record_start(self, task: str):
        self._sequence.append(task)

    def record_effect(self, parent: str, child: str):
        self._edges.add((parent, child))

    def _save_to_file(self, output_path: Path | None, data: str) -> None:
        if output_path is None:
            sys.exit('No output path specified')

        with output_path.open('w') as f:
            f.write(data)

    def render(
        self,
        renderer: ShellRenderer | DotRenderer,
        output_path: Path | None = None,
    ):
        to_save = renderer.render(sequence=self._sequence, edges=self._edges)

        if isinstance(renderer, ShellRenderer):
            print('\nExecution Plan Graph:')
            print(to_save)
        else:
            self._save_to_file(output_path, to_save)
