from starlette.responses import Response, RedirectResponse
from starlette.templating import Jinja2Templates
from decorators import web, login_required
from starlette.requests import Request
from constants.privileges import Privileges
from objects import glob
import aiohttp
import hashlib
import bcrypt
import orjson

jinja = Jinja2Templates(directory='templates')

@web(url="/")
@login_required
async def dashboard(req: Request):
    async with aiohttp.ClientSession() as sess:
        async with sess.get("https://admin.ainu.pw/api/bancho_graph") as resp:
            graph_data = orjson.loads(await resp.read())

    return jinja.TemplateResponse('index.html', {'request': req, 'graph_data': graph_data})

@web(url="/login")
async def login(req: Request):
    if req.session:
        return RedirectResponse(req.url_for("homepage"))
        
    return jinja.TemplateResponse('login.html', {'request': req})

@web(url="/submit/login", methods=["POST"])
async def _login(req: Request):
    if req.session:
        return Response("HAS AUTH")

    data = await req.form()

    if not (user := await glob.db.fetch(
        "SELECT username, password_md5, privileges, id "
        "FROM users WHERE username = %s LIMIT 1",
        [data["user"]]
    )):
        return Response("NOT FOUND")

    data_pw = hashlib.md5(data["pwd"].encode()).hexdigest().encode()
    user_pw = user["password_md5"].encode()

    if not bcrypt.checkpw(data_pw, user_pw):
        return Response("PASSWORD INCORRECT")

    if not user["privileges"] & Privileges.ACCESS:
        return Response("NO ACCESS")

    req.session.update({
        "username": user["username"],
        "id": user["id"],
        "priv": user["privileges"],
    })
    return Response("OK")


@web(url="/logout", methods=["POST"])
@login_required
async def logout(req: Request):
    req.session.clear()
    return Response("OK")


@web(url="/beatmaps/manually")
@login_required
async def rank_manually(req: Request):
    return jinja.TemplateResponse("rank_manually.html", {"request": req})