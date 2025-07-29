import inspect
from aiagentaz.core.chain import Chain
from typing import Callable

def chain(func: Callable) -> Callable:
    """Chain the functions together."""
    def wrapper(*args, **kwargs):
        if args:
            if callable(args[0]):
                res = func(*args[1:], **kwargs)
                chain = Chain(res)
                return chain.decorate(func = args[0])
            else:
                res = func(*args, **kwargs)
                return res
        else:
            res = func(**kwargs)
            return res
    return wrapper
