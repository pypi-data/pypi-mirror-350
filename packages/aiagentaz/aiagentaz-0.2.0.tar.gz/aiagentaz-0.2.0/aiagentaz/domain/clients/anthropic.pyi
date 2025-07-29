from typing import Dict, Any
from anthropic.types.message import Message

class AnthropicClient:
    def __init__(self, **kwargs: Dict[str, Any]) -> None: ...

    def generate(
        self,
        prompt: str,
        model: str,
        max_tokens: str,
        **kwargs: Dict[str, Any]
    ) -> Message: ...