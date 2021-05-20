from starlette_authlib.middleware import AuthlibMiddleware as SessionMiddleware
from starlette.staticfiles import StaticFiles
from starlette.applications import Starlette
from starlette.routing import Mount, Route
from globals import Globals
from config import config
from objects import glob
from events import web, api
import uvicorn
import cmyui
import os

routes = [
    Route(r["url"], endpoint=r["cb"], methods=r["methods"]) for r in glob.route_map
]

routes.append(Mount('/src', StaticFiles(directory="static")))

async def startup():
    Globals(web.jinja).init()

    glob.db = cmyui.AsyncSQLPool()
    await glob.db.connect(config["mysql"])

app = Starlette(routes=routes, on_startup=[startup])

app.add_middleware(SessionMiddleware, secret_key=os.urandom(24))

if __name__ == '__main__':
    uvicorn.run("server:app", host="127.0.0.1", port=3000, loop="uvloop")
