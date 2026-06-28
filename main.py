from fastapi import FastAPI, Request,HTTPException, status
from contextlib import asynccontextmanager
from fastapi.exception_handlers import (
    http_exception_handler, 
    request_validation_exception_handler
)
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from sqlalchemy import select
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.gzip import GZipMiddleware
from routers import users, candles
from database import Base, engine
from dependencies import DbSession
import models
from constants import GENERIC_ERROR_MESSAGE

@asynccontextmanager
async def lifespan(_app:FastAPI):
    #Startup
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    #Shutdown
    await engine.dispose()

app = FastAPI(lifespan=lifespan)
app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/media", StaticFiles(directory="media"), name="media")
app.add_middleware(GZipMiddleware)
templates = Jinja2Templates(directory="templates")
app.include_router(users.router, prefix="/api/users", tags=["Users"])
app.include_router(candles.router, prefix="/api/candles", tags=["Candles"])


# ---- Endpoint Home ----
@app.get("/", include_in_schema=False, name="home")
@app.get("/candles", include_in_schema=False, name="candles")
async def home(request: Request, db: DbSession, sort_by: str = ""):
    stmt = select(models.Candle)

    sort_options = {
        "name-asc": models.Candle.name.asc(),
        "name-desc": models.Candle.name.desc(),
        "price-asc": models.Candle.price.asc(),
        "price-desc": models.Candle.price.desc(),
    }

    if sort_by in sort_options:
        stmt = stmt.order_by(sort_options[sort_by])
    else:
        stmt = stmt.order_by(models.Candle.id)

    result = await db.execute(stmt)
    candles = result.scalars().all()

    return templates.TemplateResponse(
        request,
        "home.html",
        {"candles": candles, "title": "Naná Essência", "sort_by": sort_by},
    )


# ---- Candle ----
@app.get("/{candle_id}", include_in_schema=False)
async def get_candle(candle_id: int,request: Request, db: DbSession):
    result= await db.execute(select(models.Candle).where(models.Candle.id == candle_id))

    candle= result.scalars().first()

    if not candle:
        raise HTTPException(
            status_code= status.HTTP_404_NOT_FOUND,
            detail= GENERIC_ERROR_MESSAGE
        )

    return templates.TemplateResponse(request, "candle.html", {"candle": candle, "title": candle.name})



# ---- Exception Hanlder ----
@app.exception_handler(StarletteHTTPException)
async def general_http_exception_handler(request: Request, exception: StarletteHTTPException):
    message= (
        exception.detail
        if exception.detail
        else "An error ocurred. Please check your request and try again"
    )

    if request.url.path.startswith("/api"):
        return await http_exception_handler(request, exception)
    
    return templates.TemplateResponse(
        request,
        "error.html",
        {
            "status_code":exception.status_code,
            "title":exception.status_code,
            "message":message,
        },
        status_code=exception.status_code,
    )

# ---- Exception Handler for validation error ----
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exception: RequestValidationError):
     
    if request.url.path.startswith("/api"):
        return await request_validation_exception_handler(request, exception)
    
    return templates.TemplateResponse(
        request,
        "error.html",
        {
            "status_code":status.HTTP_422_UNPROCESSABLE_CONTENT,
            "title":status.HTTP_422_UNPROCESSABLE_CONTENT,
            "message":GENERIC_ERROR_MESSAGE,
        },
        status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
    )


# ---- Dashboard Admin ----
@app.get("/admin/dashboard", response_class=HTMLResponse)
def dashboard():
    return f"<h1>DASHBOARD PARA ADMIN</h1>"


# ---- Register Form ----
@app.get("/register", response_class=HTMLResponse)
def register():
    return f"<h1>REGISTRO</h1>"


