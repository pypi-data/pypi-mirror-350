from typing import Dict, Any
from openai.types.chat.chat_completion import ChatCompletionMessage

class OpenAIClient:
    def __init__(self, **kwargs: Dict[str, Any]) -> None: ...

    def generate(
        self,
        prompt: str,
        model: str,
        **kwargs: Dict[str, Any]
    ) -> ChatCompletionMessage: ...
