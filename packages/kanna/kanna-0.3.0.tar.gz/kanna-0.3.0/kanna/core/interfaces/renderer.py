from abc import ABC, abstractmethod


class PlanRenderer[T](ABC):
    """
    Base class for rendering the execution plan of a task.
    """

    @abstractmethod
    def render(
        self,
        sequence: list[str],
        edges: set[tuple[str, str]],
        **kwargs: T | None,
    ) -> None:
        """
        Render the execution plan to the specified output path.

        Args:
            output_path (Path): The path to save the rendered output.
        """
        ...
