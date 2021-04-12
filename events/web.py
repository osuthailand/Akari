from starlette.templating import Jinja2Templates
from starlette.responses import Response
from decorators import web, login_required
from starlette.requests import Request
from objects.privileges import Privileges
from objects import glob
import hashlib
import bcrypt

# install jinja and make
# the directory to /akari/templates
jinja = Jinja2Templates(directory='templates')

@web(url="/")
@login_required
async def homepage(req: Request):
    return jinja.TemplateResponse('index.html', {'request': req})

@web(url="/login", methods=["GET", "POST"])
async def login(req: Request):
    return jinja.TemplateResponse('login.html', {'request': req})

@web(url="/submit/login", methods=["POST"])
async def _login(req: Request):
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
