import importlib


class ClientConfig:
    """Configuration class for AI clients.
    
    This class handles the configuration and dynamic loading of AI client classes
    based on their module and class names.
    """

    def __init__(
            self,
            name: str,
            class_name: str,
            module_name: str
    ):
        """Initialize a new client configuration.

        Args:
            name (str): The identifier name for the client
            class_name (str): The name of the client's main class
            module_name (str): The full module path where the client class is located
        """
        self.name = name
        self.class_name = class_name
        self.module_name = module_name

    @property
    def client_class(self):
        """Dynamically load and return the client class.

        Returns:
            type: The loaded client class
        """
        module = importlib.import_module(self.module_name)
        class_name = getattr(module, self.class_name)

        return class_name


# Dictionary to store all registered client configurations
known_clients = dict()

# Register the OpenAI client configuration
known_clients["openai"] = ClientConfig(
    name="openai",
    class_name="OpenAIClient",
    module_name="aiagentaz.domain.clients.openai"
)

# Register the Gemini client configuration
known_clients["gemini"] = ClientConfig(
    name="gemini",
    class_name="GeminiClient",
    module_name="aiagentaz.domain.clients.gemini"
)

# Register the Anthropic client configuration
known_clients["anthropic"] = ClientConfig(
    name="anthropic",
    class_name="AnthropicClient",
    module_name="aiagentaz.domain.clients.anthropic"
)