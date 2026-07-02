from fastapi import APIRouter, HTTPException, status
from sqlalchemy import select
import models
from schemas import CandleAdminResponse, CandleUpdate, UserAdminCreate, UserAdminResponse
from dependencies import DbSession

router = APIRouter()

# ---- Dashboard Admin ----
@router.get("/admin/dashboard", include_in_schema=False, )
def dashboard():
    return f"<h1>DASHBOARD PARA ADMIN</h1>"
