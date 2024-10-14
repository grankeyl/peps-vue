from fastapi import APIRouter
from fastapi import HTTPException
from fastapi import Request
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from fastapi.templating import Jinja2Templates

home_panel = APIRouter()
templates = Jinja2Templates(directory="./templates")

@home_panel.get('/')
async def admin_home(request: Request):
    return templates.TemplateResponse(
        "home.html", {
            "request": request
        }
    )