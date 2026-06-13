from datetime import UTC, datetime
from sqlalchemy import DateTime, Integer, String, Text, Boolean, Float
from sqlalchemy.orm import Mapped, mapped_column
from database import Base

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    creation_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(UTC))
    is_admin: Mapped[bool] = mapped_column(Boolean, default=False)
    


class Candle(Base):
    __tablename__ = "candles"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    scent: Mapped[str] = mapped_column(String(50), nullable=False )
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    size: Mapped[int] = mapped_column(Integer, nullable=False)
    price: Mapped[float] = mapped_column(Float, nullable=False)
    cost: Mapped[float | None] = mapped_column(Float, nullable=True)
    stock: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    
    #Control de visibilidad
    is_hidden: Mapped[bool] = mapped_column(Boolean, default=False)
    creation_date: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), 
        default=lambda: datetime.now(UTC)
        )
    update_date: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), 
        default=lambda: datetime.now(UTC), 
        onupdate= lambda:datetime.now(UTC)
        )
    image_file: Mapped[str | None] = mapped_column(String(120),nullable=True)

    @property
    def has_stock(self) -> bool:
        """Retorna True si hay stock disponible, de lo contrario retorna False"""
        return self.stock > 0  
    
    @property
    def image_path(self) -> str:
        if self.image_file:
            return f"/media/candle_pic/{self.image_file}"
        return "/static/candle_pic/default.jpg"