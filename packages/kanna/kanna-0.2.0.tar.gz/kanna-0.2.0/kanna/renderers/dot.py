class DotRenderer:
    def render(self, sequence: list[str], edges: set[tuple[str, str]]) -> str:
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
        return '\n'.join(lines)
