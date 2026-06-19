from fastapi import FastAPI, Request,HTTPException, status
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.gzip import GZipMiddleware
from schemas import CandleCreate, CandlePublicResponse
from sqlalchemy import select
from routers import users, candles
from database import Base, engine
from dependencies import DbSession
import models


Base.metadata.create_all(bind=engine)

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/media", StaticFiles(directory="media"), name="media")

app.add_middleware(GZipMiddleware)

templates = Jinja2Templates(directory="templates")


app.include_router(users.router, prefix="/api/users", tags=["Users"])
app.include_router(candles.router, prefix="/api/candles", tags=["Candles"])


# ---- Endpoint Home ----
@app.get("/", include_in_schema=False)
@app.get("/candles", include_in_schema=False)
def home(request: Request, db: DbSession):
    result= db.execute(select(models.Candle))

    candles= result.scalars().all()

    return templates.TemplateResponse(request, "home.html", {"candles":candles, "title": "Catálogo de velas"})


@app.get("/register", response_class=HTMLResponse)
def register():
    return f"<h1>REGISTRO</h1>"


@app.get("/{candle_id}", include_in_schema=False)
def get_candle(candle_id: int,request: Request, db: DbSession):
    result= db.execute(select(models.Candle).where(models.Candle.id == candle_id))

    candle= result.scalars().first()

    if not candle:
        raise HTTPException(
            status_code= status.HTTP_404_NOT_FOUND,
            detail= "Candle not found"
        )

    return templates.TemplateResponse(request, "candle.html", {"candle": candle, "title": candle.name})


@app.get("/admin/dashboard", response_class=HTMLResponse)
def dashboard():
    return f"<h1>DASHBOARD PARA ADMIN</h1>"
