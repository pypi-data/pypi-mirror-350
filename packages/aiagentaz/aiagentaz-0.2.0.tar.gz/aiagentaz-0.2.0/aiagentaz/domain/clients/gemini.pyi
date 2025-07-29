from typing import Dict, Any

class GeminiClient:
    def __init__(self, **kwargs: Dict[str, Any]) -> None: ...

    def generate(
        self, 
        prompt: str, 
        model: str, 
        **kwargs: Dict[str, Any]
    ) -> str: ... 