from pathlib import Path
from typing import Any

from kanna.core.interfaces.renderer import PlanRenderer


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

    def render(
        self,
        renderer: PlanRenderer[Any],
        output_path: Path | None = None,
    ):
        renderer.render(
            sequence=self._sequence, edges=self._edges, output_path=output_path
        )
