import click
from typing import NamedTuple
from functools import wraps
from pathlib import Path
from recodex.api import ApiClient
from recodex.config import UserContext


class ReCodExContext(NamedTuple):
    api_client: ApiClient
    config_dir: Path
    data_dir: Path
    user_context: UserContext


def make_pass_decorator(selector):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            ctx = click.get_current_context()
            obj = selector(ctx.find_object(ReCodExContext))
            return ctx.invoke(f, obj, *args, **kwargs)
        return wrapper
    return decorator


pass_api_client = make_pass_decorator(lambda context: context.api_client)
pass_config_dir = make_pass_decorator(lambda context: context.config_dir)
pass_data_dir = make_pass_decorator(lambda context: context.data_dir)
pass_user_context = make_pass_decorator(lambda context: context.user_context)
