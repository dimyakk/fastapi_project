from fastapi import FastAPI, Request,HTTPException, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import HTMLResponse, JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.gzip import GZipMiddleware
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

GENERIC_ERROR_MESSAGE = (
    "A página que você buscou não foi encontrada...\n"
    "Mas não se preocupe, viemos resgatar você!"
)

# ---- Endpoint Home ----
@app.get("/", include_in_schema=False, name="home")
@app.get("/candles", include_in_schema=False, name="candles")
def home(request: Request, db: DbSession, sort_by: str = ""):
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

    result = db.execute(stmt)
    candles = result.scalars().all()

    return templates.TemplateResponse(
        request,
        "home.html",
        {"candles": candles, "title": "Naná Essência", "sort_by": sort_by},
    )


# ---- Candle ----
@app.get("/{candle_id}", include_in_schema=False)
def get_candle(candle_id: int,request: Request, db: DbSession):
    result= db.execute(select(models.Candle).where(models.Candle.id == candle_id))

    candle= result.scalars().first()

    if not candle:
        raise HTTPException(
            status_code= status.HTTP_404_NOT_FOUND,
            detail= "A página que você buscou não foi encontrada...\nMas não se preocupe, viemos resgatar você!"
        )

    return templates.TemplateResponse(request, "candle.html", {"candle": candle, "title": candle.name})



# ---- Exception Hanlder ----
@app.exception_handler(StarletteHTTPException)
def general_http_exception_handler(request: Request, exception: StarletteHTTPException):
    message= (
        exception.detail
        if exception.detail
        else "An error ocurred. Please check your request and try again"
    )

    if request.url.path.startswith("/api"):
        return JSONResponse(
            status_code= exception.status_code,
            content={"detail": message}
        )
    
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
def validation_exception_handler(request: Request, exception: RequestValidationError):
     
    if request.url.path.startswith("/api"):
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            content={"detail": exception.errors()},
        )
    
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


