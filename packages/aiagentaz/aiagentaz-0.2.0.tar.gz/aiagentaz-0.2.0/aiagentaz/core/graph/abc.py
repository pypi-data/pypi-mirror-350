from __future__ import annotations
from abc import abstractmethod
from collections.abc import Iterable
from typing import Any

class DependencyABC:
    """Contains basic methods required to set up a dependency between nodes"""

    def __init__(self):
        self.input_from_upstream_node: Any = None

    @property
    def roots(self) -> Iterable[DependencyABC]:
        """List of root nodes. These are nodes that have no upstream dependencies
        
        a.k.a the starting point"""
        raise NotImplementedError()
    
    @property
    def leaves(self) -> Iterable[DependencyABC]:
        """List of leaf nodes. These are nodes that have no downstream dependencies
        
        a.k.a the ending point"""
        raise NotImplementedError()
    
    @abstractmethod
    def execute_task(self, other: DependencyABC) -> None:
        """Execute the task of this node"""
        raise NotImplementedError() 
    
    def __lshift__(self, other: DependencyABC) -> None:
        """Implements the << operator to set up a dependency between two nodes.
        For example: Task1 << Task2 will set up a dependency between Task1 and Task2,
        where Task1 will execute before Task2.
        
        args:
            other: The node that this node depends on. I.e. Task2 in the example above"""
        raise NotImplementedError(
            "The << operator is not supported. Please use the >> operator instead."
        )
    
    def __rshift__(self, other: DependencyABC) -> DependencyABC:
        """Implements the >> operator to set up a dependency between two nodes.
        For example: Task1 >> Task2 will set up a dependency between Task1 and Task2,
        where Task2 will execute after Task1.
        
        args:
            other: The downstream node that this node depends on. I.e. Task2 in the example above"""
        other.input_from_upstream_node = self.execute_task()
        return other
    