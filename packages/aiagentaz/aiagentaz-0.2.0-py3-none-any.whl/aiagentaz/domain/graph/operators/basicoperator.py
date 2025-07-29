from typing import Callable, Any

from aiagentaz.core.graph.node import BaseNode

class BasicOperator(BaseNode):
    """Basic operator class. This is a basic operator that can be used to create a graph.
    
    Operators are the building blocks of the graph. They are the nodes that perform the actual work.
    """

    def __init__(self, task_id: str, task: Callable):
        super().__init__()
        self.task_id = task_id
        self.task = task

    @property
    def node_id(self) -> str:
        return self.task_id
    
    def execute_task(self) -> Any:
        """Execute the task"""
        if callable(self.task):
            if 'input_from_upstream_node' in self.task.__code__.co_varnames:
                return self.task(input_from_upstream_node=self.input_from_upstream_node)
            raise ValueError(f"The task {self.task_id} must have an input_from_upstream_node parameter")
        raise TypeError(f"The task {self.task_id} is not callable")
    