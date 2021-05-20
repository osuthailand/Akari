from typing import Callable
from objects import glob
from constants.privileges import Privileges
from objects.responses import ajson
from starlette.requests import Request
from starlette.responses import RedirectResponse
from functools import wraps

# this is the decorator used
# to insert all endpoints
# into glob.route_map where
# we then add it to starlette's routes
def web(url: str, methods: list = ["GET"]) -> Callable:
    def callback(cb: Callable) -> Callable:
        glob.route_map.append({
            "cb": cb,
            "url": url,
            "methods": methods
        })

    return callback

def login_test(cb: Callable):
    def decorator(f):
        @wraps(f)
        async def wrapper(req: Request, *args, **kwargs):
            if not req["session"]:
                return RedirectResponse("/login")

            return await cb(req, *args, **kwargs)

        return wrapper

    return decorator

def login_required(cb: Callable) -> Callable:
    check = login_test(cb)
    
    if check:
        return check(cb)

    return check

def required_params(params: list[str]):
    def decorator(cb: Callable):
        @wraps(cb)
        async def wrapper(req: Request, *args, **kwargs):
            if not all(x in req.query_params for x in params):
                return ajson({"error": "missing params"})

            return await cb(req, *args, **kwargs)

        return wrapper

    return decorator

def required_priv(priv = Privileges.ACCESS):
    def decorator(cb: Callable):
        @wraps(cb)
        async def wrapper(req: Request, *args, **kwargs):
            if not req.session["priv"] & priv:
                return RedirectResponse("/no_perms")

            return await cb(req, *args, **kwargs)

        return wrapper

    return decorator
