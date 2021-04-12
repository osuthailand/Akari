from starlette.templating import Jinja2Templates
from starlette.responses import RedirectResponse, PlainTextResponse
from decorators import web, login_required
from starlette.requests import Request

# install jinja and make
# the directory to /akari/templates
jinja = Jinja2Templates(directory='templates')

@web(url="/")
@login_required
async def homepage(req: Request):
    return jinja.TemplateResponse('index.html', {'request': req})

@web(url="/submit/login", methods=["POST"])
async def _login(req: Request):
    return RedirectResponse(url="/", status_code=303)

@web(url="/login")
async def login(req: Request):
    return jinja.TemplateResponse('index.html', {'request': req})
