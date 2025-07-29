from typing import Literal, Any, ContextManager, overload

from clients.openai import OpenAIClient
from clients.gemini import GeminiClient

class Agent:
    client: str
    client_kwargs: dict[str, Any]
    
    def __init__(
            self, 
            client: Literal["openai", "gemini"], 
            /, 
            **kwargs: Any
        ) -> None: ...

    @overload
    def get_client(
            self, 
            client: Literal["openai"], 
            **kwargs: Any
        ) -> ContextManager[OpenAIClient]: ...
    
    @overload
    def get_client(
            self, 
            client: Literal["gemini"], 
            **kwargs: Any
        ) -> ContextManager[GeminiClient]: ...
