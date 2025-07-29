"""
Agent module for handling client interactions and generation requests.

This module provides the main functionalities for setting up clients and generating
responses using different AI service providers.
"""

from contextlib import contextmanager
from pydantic import BaseModel, Field, field_validator

from ..core.clients import known_clients
from ..core.request import Request

class Agent(BaseModel):
    """Base Agent class for handling AI client interactions.
    
    This class serves as a foundation for AI agents, managing client configuration
    and initialization parameters.
    
    Attributes:
        client: The required AI client instance (must be a string).
        client_kwargs: Dictionary storing client configuration parameters.
    """
    client_kwargs: dict = Field(default_factory=dict, description="Client configuration parameters including the client instance")

    @field_validator('client_kwargs')
    def validate_client(cls, v: dict) -> dict:
        """Validate that client exists in client_kwargs and is a non-None string."""
        if 'client' not in v:
            raise ValueError("client must be provided.")
        if not isinstance(v['client'], str):
            raise ValueError("client must be a string")
        if v['client'] is None:
            raise ValueError("client cannot be None")
        return v

    def __init__(self, client: str, **kwargs) -> None:
        """Initialize the Agent with a required client and additional parameters.
        
        Args:
            client: The AI client instance (required string).
            kwargs: Additional keyword arguments for client configuration.
        """
        kwargs["client"] = client
        super().__init__(client_kwargs=kwargs)

    @contextmanager
    def get_client(self, client: str, **kwargs):
        """Context manager for handling client initialization and cleanup.
        
        Args:
            client (str): The name of the client to initialize (required).
            kwargs: Additional keyword arguments passed to the client constructor.
            
        Yields:
            object: An initialized client instance or None if initialization fails.
            
        Raises:
            ValueError: If client is None or not a string.
        """
        if not client:
            raise ValueError("client parameter is required")
            
        request = Request(client)

        try:
            config = known_clients[client]
            yield config.client_class(**kwargs)
        except Exception as e:
            print(f"Error initializing client: {e}")
            yield None
        finally:
            pass

    def generate(self, model=None, prompt=None, **kwargs):
        """Generate a response using the specified client and configuration.

        Args:
            model (str): The model to use for generation. Defaults to None.
            prompt (str): The input prompt for generation. Defaults to None.
            kwargs: Additional keyword arguments for client configuration and generation.

        Returns:
            object: The generation result from the client, or 0 if an error occurs.

        Example:

            response = generate(
                client="openai",
                prompt="Write a poem",
                api_key="your-key",
                model="gpt-4"
                
            )
        """
        # Prepare arguments for the generation call
        call_kwargs = kwargs  # The additional arguments passed to the call to this function

        # Initialize client and generate response
        with self.get_client(**self.client_kwargs) as client:
            if client:
                try:
                    res = client.generate(prompt=prompt, model=model, **call_kwargs)
                    return res
                except Exception as e:
                    print(f"Error during generation: {e}")

