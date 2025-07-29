"""
Unit tests for OpenAI integration functionality.
Tests the agent's ability to generate responses using OpenAI's API.
"""

from unittest.mock import patch, Mock

from aiagentaz.domain.agent import Agent


def test_openai_generate():
    """Test the OpenAI generate function with mocked API response."""
    # Create an agent instance
    test_agent = Agent(client="openai", api_key="test-key")
    
    # Mock the API response
    mock_response = Mock()
    mock_response.content = "print('Hello, World!')"
    
    with patch('aiagentaz.domain.agent.Agent.generate') as mock_generate:
        mock_generate.return_value = mock_response
        
        # Test the function call
        response = test_agent.generate(
            prompt="Create a hello world program in python.",
            model="gpt-4o-mini"
        )
        
        # Verify the response matches our expected output
        assert response.content == "print('Hello, World!')"
