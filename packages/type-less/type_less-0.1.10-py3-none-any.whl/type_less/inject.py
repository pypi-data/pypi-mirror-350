from .inference import guess_return_type
from functools import wraps
from typing import Callable, TypeVar


def fill_type_hints(func: Callable, use_literals=True):
    if not getattr(func, "__annotations__", None):
        func.__annotations__ = {}

    if not "return" in func.__annotations__:
        func.__annotations__["return"] = guess_return_type(func, use_literals=use_literals)


T = TypeVar("T")
def fastapi_app_inject_types(app: T, use_literals=True) -> T:
    """
    Auto-injects return types into FastAPI untyped routes.

    Can be run before or after route initialization
    Arguments:
        app: FastAPI Application
    """
    routes = getattr(app, 'routes', None)
    if not type(routes) is list:
        raise ValueError("Invalid app provided, no routes found.  Please be sure this is a FastAPI app.")
    for route in routes:
        endpoint = getattr(route, "endpoint", None)
        if not endpoint:
            raise ValueError(f"Route {route} is missing an endpoint function")
        fill_type_hints(endpoint, use_literals=use_literals)
    
    # Auto-fill type hings 
    app_add_route = app.router.add_api_route
    @wraps(app_add_route)
    def add_route_injected(path: str, func, *args, **kwargs):
        fill_type_hints(func, use_literals=use_literals)
        app_add_route(path=path, endpoint=func, *args, **kwargs)
    app.router.add_api_route = add_route_injected

    return app