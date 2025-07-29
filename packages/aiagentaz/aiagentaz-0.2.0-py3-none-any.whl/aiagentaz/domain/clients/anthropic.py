"""
Anthropic client implementation for AI generation tasks.

This module provides the Anthropic-specific client implementation for making API calls
to Anthropic's services and handling responses.
"""


from anthropic import Anthropic
from anthropic.types.message import Message

class AnthropicClient:
    """
    Client class for interacting with Anthropic's API services.
    
    Handles authentication and generation requests to OpenAI's models.
    """
    def __init__(self, **kwargs) -> None:
        """
        Initialize the Anthropic client.
        
        Args:
            kwargs: Additional configuration parameters
        """
        self.client = Anthropic(**kwargs)


    def generate(self, prompt: str, model: str, max_tokens: str, **kwargs) -> Message:
        """
        Generate a response from Anthropic's model.
        
        Args:
            prompt (str): The input prompt for generation
            model (str): The model to use for generation
            max_tokens (int): Maximum number of tokens
            kwargs: Additional configuration parameters
        """

        if not prompt or not model or not max_tokens:
            raise ValueError("prompt and model and max_tokens parameters are required.")

        messages=[
            {"role": "user", "content": prompt}
        ]

        # Generate a response
        try:
            response = self.client.messages.create(
                model=model,
                max_tokens= max_tokens,
                messages=messages,
                **kwargs
            )

            return response
        except Exception as e:
            print(f"Anthropic API error: {e}")

    