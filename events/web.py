from starlette.responses import Response, RedirectResponse
from starlette.templating import Jinja2Templates

from decorators import (
    web, login_required,
    required_priv 
)

from starlette.requests import Request
from constants.privileges import Privileges
from objects import glob
import aiohttp
import hashlib
import bcrypt
import orjson
import datetime

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

@web(url="/no_perms")
@login_required
async def no_perms(req: Request):
    return jinja.TemplateResponse("errors/no_perms.html", {"request": req})

@web(url="/reported")
@login_required
@required_priv(Privileges.MANAGE_REPORTS)
async def reports(req: Request):
    if not (reported_users := await glob.db.fetchall(
            "SELECT r.id, r.from_uid, r.to_uid, r.reason, r.time, r.assigned, u.username, us.username as reported_username FROM reports r INNER JOIN users u ON r.from_uid = u.id INNER JOIN users_stats us ON r.to_uid = us.id ORDER BY time DESC LIMIT 50"
        )):
        return Response("wtf?")

    for user in reported_users:
        user["time"] = datetime.datetime.fromtimestamp(user["time"]).strftime('%Y-%m-%d %H:%M:%S')
        user["assigned"] = {0: "NOT CHECKED", -1: "SOLVED", -2: "INVALID"}[user["assigned"]]

    return jinja.TemplateResponse("report.html", {"request": req, "reports": reported_users})


@web(url="/beatmaps/manually")
@login_required
async def rank_manually(req: Request):
    return jinja.TemplateResponse("rank_manually.html", {"request": req})