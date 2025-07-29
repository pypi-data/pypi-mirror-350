from aiagentaz.domain.chain import chain
import pytest

def test_chain_single_function():
    @chain
    def f():
        return "1"
    
    assert f() == "1"

def test_chain_single_function_with_argument():
    @chain
    def f(customer_id: str = "1"):
        return customer_id
    
    assert f() == "1"

def test_chain_single_function_with_keyword_argument():
    @chain
    def f(customer_id: str):
        return customer_id
    
    assert f(customer_id = "2") == "2"

def test_chain_exception_for_missing_previous_response():
    @chain
    def f():
        return "1"

    @f
    def g():
        return "2"
    
    with pytest.raises(ValueError):
        g()

def test_chain():
    @chain
    def f():
        return "1"
    
    @f
    def g(previous_response: str = None):
        return previous_response + "2"
    
    @g
    def h(previous_response: str = None):
        return previous_response + "3"
    
    assert h() == "123"


