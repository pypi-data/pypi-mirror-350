import inspect
from typing import Callable

class Chain:
    """Chain class for handling chain of prompts."""
    
    def __init__(self, res: str = None):
        self.res = res

    def has_keyword_argument(self, func: Callable, keyword: str) -> bool:
        """Check if the function has a keyword argument."""
        return keyword in inspect.signature(func).parameters
    
    def decorate(self, func: Callable):
        """Decorate the function with the previous response."""
        def wrapper(*args, **kwargs):
            if self.has_keyword_argument(func, "previous_response"):
                if args:
                    if callable(args[0]):
                        kwargs = kwargs.copy()
                        kwargs["previous_response"] = self.res
                        res = func(*args[1:], **kwargs)
                        chain = Chain(res)
                        return chain.decorate(func = args[0])
                    else:
                        kwargs = kwargs.copy()
                        kwargs["previous_response"] = self.res
                        res = func(*args, **kwargs)
                        return res
                else:
                    kwargs = kwargs.copy()
                    kwargs["previous_response"] = self.res
                    res = func(**kwargs)
                    return res
            else:
                raise ValueError(f"The function {func.__name__} must have a 'previous_response' keyword argument.")
        return wrapper
        
        
