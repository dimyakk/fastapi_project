from fastapi import Request,APIRouter, HTTPException, status
from sqlalchemy import select
import models
from schemas import CandleAdminResponse, CandleUpdate, UserAdminCreate, UserAdminResponse
from dependencies import DbSession
from fastapi.templating import Jinja2Templates
from datetime import datetime

router = APIRouter()
templates = Jinja2Templates(directory="templates/admin")
templates.env.globals["now"] = datetime.now

# ---- Dashboard Admin ----
@router.get("/", include_in_schema=False, name="dashboard_home")
@router.get("/dashboard", include_in_schema=False, name="dashboard")
async def dashboard(request:Request):
    return templates.TemplateResponse(
        request,
        "dashboard.html",
        {"title": "Dashboard"}
    )


@router.get("/candles", include_in_schema=False, name="candles")
async def candles(request:Request):
    return templates.TemplateResponse(
        request,
        "candles.html",
        {"title": "Velas"},
    )


@router.get("/users", include_in_schema=False, name="users")
async def users(request:Request):
    return templates.TemplateResponse(
        request,
        "users.html",
        {"title": "Usuarios"},
    )


@router.get("/config", include_in_schema=False, name="config")
async def configuration(request:Request):
    return templates.TemplateResponse(
        request,
        "config.html",
        {"title": "Configuracion"},
    )