class ShellRenderer:
    """
    Renders a recorded execution graph in the terminal as ASCII art, showing
    both dependency relationships and the actual call sequence.
    """

    def render(self, sequence: list[str], edges: set[tuple[str, str]]) -> str:
        # 1) Preserve unique tasks in invocation order
        unique_tasks: list[str] = []
        for task in sequence:
            if task not in unique_tasks:
                unique_tasks.append(task)

        # 2) Map each task to its invocation index
        index_map = {task: idx + 1 for idx, task in enumerate(unique_tasks)}

        # 3) Group dependencies by source task
        dep_map: dict[str, list[str]] = {task: [] for task in unique_tasks}
        for src, dst in sorted(edges):
            dep_map[src].append(dst)

        # 4) Build ASCII lines
        lines: list[str] = []
        for i, task in enumerate(unique_tasks):
            # Node header
            lines.append(f'[{index_map[task]}] {task}')

            # Dependency edges
            for child in dep_map[task]:
                lines.append(f'    ├─ dep → {child}')

            # Sequence edge to next task
            if i < len(unique_tasks) - 1:
                next_task = unique_tasks[i + 1]
                lines.append(f'    └─ seq → {next_task}')

            # Blank line for readability
            lines.append('')

        return '\n'.join(lines)
