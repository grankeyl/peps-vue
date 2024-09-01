from fastapi import APIRouter
from fastapi import HTTPException
from fastapi import Request
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from fastapi.templating import Jinja2Templates

# Экземпляр APIRouter
router = APIRouter()
router_key = "/api/tasks"

@router.post('{}/create'.format(router_key))
async def user_create(request: Request):
    pass