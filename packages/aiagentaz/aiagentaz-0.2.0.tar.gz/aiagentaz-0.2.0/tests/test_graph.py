from aiagentaz.domain.graph.operators.basicoperator import BasicOperator
import pytest

def test_basic_operator():

    def test_task_1(input_from_upstream_node: str):
        return "test_result_1"
    
    def test_task_2(input_from_upstream_node: str):
        return f"test_result_2: {input_from_upstream_node}"
    
    task_1 = BasicOperator("test_task_1", test_task_1)
    task_2 = BasicOperator("test_task_2", test_task_2)
    
    workflow = task_1 >> task_2
    
    assert workflow.execute_task() == "test_result_2: test_result_1"