"""
OpenAI client implementation for AI generation tasks.

This module provides the OpenAI-specific client implementation for making API calls
to OpenAI's services and handling responses.
"""

from openai import OpenAI
from openai.types.chat.chat_completion import ChatCompletionMessage

class OpenAIClient:
    """Client class for interacting with OpenAI's API services.
    
    Handles authentication and generation requests to OpenAI's models.
    """
    def __init__(self, **kwargs) -> None:
        """Initialize the OpenAI client.
        
        Args:
            kwargs: Additional configuration parameters
        """
        self.client = OpenAI(**kwargs)

    def generate(self, prompt: str, model: str, **kwargs) -> ChatCompletionMessage:
        """Generate a response from OpenAI's model.
        
        Args:
            prompt (str): The input prompt for generation
            model (str): The model to use for generation
            kwargs: Additional configuration parameters

        Returns:
            ChatCompletionMessage: The generated response message
        """
        if not prompt or not model:
            raise ValueError("Both prompt and model parameters are required.")

        messages=[
            {"role": "user", "content": prompt}
        ]

        # Generate a response
        try:
            response = self.client.chat.completions.create(
                model=model,
                messages=messages,
                **kwargs
            )

            return response.choices[0].message
        except Exception as e:
            print(f"OpenAI API error: {e}")
