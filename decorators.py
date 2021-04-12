from typing import Callable
from objects import glob
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

def user_test(cb: Callable):
    def decorator(f):
        @wraps(f)
        async def wrapper(req: Request, *args, **kwargs):
            if not req["session"]:
                return RedirectResponse(url="/", status_code=303)

            return cb(req, *args, **kwargs)

        return wrapper

    return decorator

def login_required(cb: Callable) -> Callable:
    check = user_test(cb)
    
    if check:
        return check(cb)

    return check