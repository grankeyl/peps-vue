from fastapi import APIRouter
from fastapi import HTTPException
from fastapi import Request
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse

# Экземпляр APIRouter
router = APIRouter()
router_key = "/api/misc"

