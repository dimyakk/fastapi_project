from fastapi import Request,APIRouter, HTTPException, status
from sqlalchemy import select, func
import models
from schemas import CandleAdminResponse, CandleUpdate, UserAdminCreate, UserAdminResponse
from dependencies import DbSession
from fastapi.templating import Jinja2Templates
from datetime import datetime, UTC

router = APIRouter()
templates = Jinja2Templates(directory="templates/admin")
templates.env.globals["now"] = datetime.now


today = datetime.now(UTC)

start_of_month = datetime(
    year=today.year,
    month=today.month,
    day=1,
    tzinfo=UTC
)


# ---- Dashboard Admin ----
@router.get("/", include_in_schema=False, name="dashboard_home")
@router.get("/dashboard", include_in_schema=False, name="dashboard")
async def dashboard(request:Request, db:DbSession):

    stmt = select(models.Candle)
    result = await db.execute(stmt)
    candles = result.scalars().all()

    total_candles = await db.scalar(
        select(func.count()).select_from(models.Candle)
    )

    new_candles = await db.scalar(
        select(func.count()).select_from(models.Candle).where(models.Candle.creation_date >= start_of_month)
    )

    in_stock = await db.scalar(
        select(func.count()).select_from(models.Candle).where(models.Candle.stock > 0)
    )

    out_stock = total_candles - in_stock

    hidden_candles = await db.scalar(
        select(func.count()).select_from(models.Candle).where(models.Candle.is_hidden == True)
    )

    total_users = await db.scalar(
        select(func.count()).select_from(models.User)
    )

    new_users = await db.scalar(
        select(func.count()).select_from(models.User).where(models.User.creation_date >= start_of_month)
    )    

    return templates.TemplateResponse(
        request,
        "dashboard.html",
        {
            "title": "Dashboard",
            "candles": candles,
            "total_candles": total_candles,
            "new_candles": new_candles,
            "in_stock": in_stock,
            "out_stock": out_stock,
            "hidden_candles": hidden_candles,
            "total_users": total_users,
            "new_users": new_users,
            }
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