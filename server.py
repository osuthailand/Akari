from starlette_authlib.middleware import AuthlibMiddleware as SessionMiddleware
from starlette.applications import Starlette
from starlette.staticfiles import StaticFiles
from starlette.routing import Mount, Route
from config import config
from globals import Globals
from events import web
from objects import glob
import cmyui
import os

routes = [
    # loop through the list
    # of endpoints and finally
    # add them to the routes
    Route(r["url"], endpoint=r["cb"], methods=r["methods"]) for r in glob.route_map
]


routes.append(Mount('/src', StaticFiles(directory="static")))

async def startup():
    # inject all global functions
    # into jinja :smirk:
    Globals(web.jinja).init()
    for r in glob.route_map:
        print(r["cb"].__name__)


    # connect to the mysql
    glob.db = cmyui.AsyncSQLPool()
    await glob.db.connect(config["mysql"])

app = Starlette(routes=routes, on_startup=[startup])

# add the session middleware.
# this is used for logins.
app.add_middleware(SessionMiddleware, secret_key=os.urandom(24))
