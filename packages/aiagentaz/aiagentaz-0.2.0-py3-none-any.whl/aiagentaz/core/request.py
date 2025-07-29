from .clients import known_clients


class Request:
    """Base class for handling AI service requests.

    This class manages the client configuration and validation for AI service requests.
    It ensures that only known and properly configured clients can be used.
    """

    def __init__(self, client: str | None) -> None:
        """Initialize a new Request instance.

        Args:
            client (str | None): The identifier for the AI client to be used.
                               Must be a key present in known_clients.
                               If None, no client will be set.
        """
        self.client = None

        # Only process if a client was provided
        if client is not None:
            # Check if the provided client is a string identifier
            if isinstance(client, str):
                # Validate that the client exists in our known clients registry
                if client in known_clients:
                    self.client = client