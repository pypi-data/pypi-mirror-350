from aiagentaz.core.graph.abc import DependencyABC

from abc import abstractmethod
from typing import Any



class BaseNode(DependencyABC):
    """Base class for all nodes in the graph"""

    def __init__(self):
        super().__init__()

    @property
    @abstractmethod
    def node_id(self) -> str:
        """Unique identifier for the node"""
        raise NotImplementedError()
    