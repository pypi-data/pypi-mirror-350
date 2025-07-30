import functools
from ..schema.response import ResponseModel


def response_handler(
    model: type[ResponseModel] | None = None,
    status_code: int = 200,
    skip: bool = False
):
    def decorator(func):
        func.__dict__['__status_code__'] = status_code

        if model:
            func.__dict__['__response_model__'] = model

        if skip:
            func.__dict__['__skip_handler__'] = skip

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)

        return wrapper

    return decorator
