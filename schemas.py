from datetime import datetime
from pydantic import BaseModel, ConfigDict, EmailStr, Field


# ===== SCHEMAS FOR USERS =====


class UserBase(BaseModel):

    username: str = Field(min_length=1, max_length=50)
    email: EmailStr = Field(max_length=120)


class UserPublicCreate(UserBase):
    pass

class UserAdminCreate(UserPublicCreate):

    is_admin: bool = Field(default=False, description="Define si un usuario tendra permisos de administrador")


class UserUpdate(UserBase):

    username: str | None = Field(default=None, min_length=1, max_length=50)
    email: EmailStr | None = Field(default=None, max_length=120)


class UserPublicResponse(UserBase):

    model_config = ConfigDict(from_attributes=True)

    id: int
    creation_date: datetime

class UserAdminResponse(UserPublicResponse):

    is_admin: bool



# ===== SCHEMAS FOR CANDLES =====


class CandleBase(BaseModel):

    name: str = Field(..., min_length=1, max_length=100)
    scent: str = Field(..., min_length=1, max_length=100)
    description: str | None = Field(default=None)
    size: int = Field(..., gt=0, description="Tamaño en gramos (gr)")
    price: float = Field(..., gt=0, description="Precio de venta al publico")


class CandleCreate(CandleBase):

    stock: int = Field(default=0, ge=0, description="Inventario inicial")
    cost: float = Field(..., gt=0, description="Costo de materiales y fabricacion")
    is_hidden: bool = Field(default=False, description="Si es True no se muestra a clientes")


class CandleUpdate(CandleBase):

    name: str | None= Field(default=None, min_length=1, max_length=100)
    scent: str | None= Field(default=None, min_length=1, max_length=100)
    description: str | None = Field(default=None)
    size: int | None = Field(default=None, gt=0, description="Tamaño en gramos (gr)")
    price: float | None= Field(default=None, gt=0, description="Precio de venta al publico")

class CandlePublicResponse(CandleBase):

    model_config = ConfigDict(from_attributes=True)

    id : int
    image_path: str
    has_stock: bool = Field(..., description="Indica si hay disponibilidad")

class CandleAdminResponse(CandlePublicResponse):

    stock: int = Field(..., ge=0, description="Inventario exacto en deposito")
    cost: float = Field(..., gt=0, description="Costo unitario")
    is_hidden: bool = Field(default=False, description="Estado de ocultamiento en catalogo")
    creation_date: datetime
    update_date: datetime
