from typing import TypedDict, Unpack

from kanna.core.interfaces.renderer import PlanRenderer


class ExtendedOptions(TypedDict):
    output_path: str


class DotRenderer(PlanRenderer[Unpack[ExtendedOptions]]):
    def _save_on_disk(self, output_path: str, draw: str) -> None:
        """
        Save the rendered graph to a file.

        Args:
            output_path (str): The path to save the rendered output.
            draw (str): The rendered graph as a string.
        """
        with open(output_path, 'w') as f:
            f.write(draw)

    def render(
        self,
        sequence: list[str],
        edges: set[tuple[str, str]],
        **kwargs: Unpack[ExtendedOptions],
    ) -> None:
        lines = [
            'digraph Execution {',
            '    // Top-to-bottom layout',
            '    rankdir=TB;',
            '    bgcolor="transparent";',
            '',
            '    // Default node style: doublecircle, filled with light gray, subtle shadow',
            '    node [',
            '        shape=doublecircle',
            '        style="filled,shadow"',
            '        fillcolor="#eaecee"',
            '        color="#34495e"',
            '        fontname="Arial"',
            '        fontsize=12',
            '        fontcolor="#34495e"',
            '    ];',
            '',
            '    // Default edge style',
            '    edge [',
            '        arrowhead=vee',
            '        arrowsize=0.8',
            '        penwidth=1.2',
            '        fontname="Arial"',
            '        fontsize=10',
            '        fontcolor="#95a5a6"',
            '    ];',
            '',
        ]

        seen: set[str] = set()
        for idx, task in enumerate(sequence, start=1):
            if task not in seen:
                seen.add(task)
                label = f'{task.replace("_", " ").title()}\\n#{idx}'
                lines.append(f'    "{task}" [label="{label}"];')
        lines.append('')

        for src, dst in sorted(edges):
            lines.append(f'    "{src}" -> "{dst}" [color="#34495e"];')
        lines.append('')

        for prev, nxt in zip(sequence, sequence[1:]):
            lines.append(
                f'    "{prev}" -> "{nxt}" [style=dashed, color="#95a5a6"];'
            )

        lines.append('}')
        self._save_on_disk(
            draw='\n'.join(lines),
            output_path=kwargs.get('output_path', './execution_graph.dot'),
        )
