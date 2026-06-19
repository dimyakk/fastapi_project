from fastapi import APIRouter, HTTPException, status
from sqlalchemy import select
import models
from schemas import CandleCreate, CandlePublicResponse, CandleAdminResponse, CandleUpdate
from dependencies import DbSession


router = APIRouter()


# ---- Create e new candle ----

@router.post("", response_model=CandleAdminResponse, status_code=status.HTTP_201_CREATED)
def new_candle(candle: CandleCreate, db: DbSession):
    result= db.execute(
        select(models.Candle).where(models.Candle.name == candle.name)
    )
    
    existing_candle = result.scalars().first()

    if existing_candle:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Candle already exists"
        )
    
    new_candle = models.Candle(
        name= candle.name,
        scent= candle.scent,
        description= candle.description,
        size= candle.size,
        price= candle.price,
        stock= candle.stock,
        cost= candle.cost
    )


    db.add(new_candle)
    db.commit()
    db.refresh(new_candle)

    return new_candle

# ---- Get a candle ----

@router.get("/{candle_id}", response_model=CandlePublicResponse)
def get_candle(candle_id: int, db: DbSession):
    result= db.execute(select(models.Candle).where(models.Candle.id == candle_id))

    candle= result.scalars().first()

    if not candle:
        raise HTTPException(
            status_code= status.HTTP_404_NOT_FOUND,
            detail= "Candle not found"
        )

    return candle


# ---- Get a candles list ----

@router.get("", response_model=list[CandlePublicResponse])
def get_all_candles(db: DbSession):
    result= db.execute(select(models.Candle))

    candles= result.scalars().all()

    return candles


# ---- Candle Update ----

@router.patch("/{candle_id}", response_model=CandlePublicResponse)
def update_candle(candle_id:int, candle_update:CandleUpdate, db:DbSession):

    result = db.execute(select(models.Candle).where(models.Candle.id == candle_id))
    candle = result.scalars().first()

    if not candle:
        raise HTTPException(
        status_code= status.HTTP_404_NOT_FOUND,
        detail= "Candle not found"
        )

    if candle_update.name is not None and candle_update.name != candle.name:
        result = db.execute(select(models.Candle).where(models.Candle.name == candle_update.name))

        existing_candle= result.scalars().first()

        if existing_candle:
            raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail= "Candle name already exists"
        )
    
    update_data = candle_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(candle,field,value)
    
    db.commit()
    db.refresh(candle)

    return candle


# ---- Delete a candle ----

@router.delete("/{candle_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_candle(candle_id: int, db: DbSession):
    result = db.execute(select(models.Candle).where(models.Candle.id == candle_id))
    candle = result.scalars().first()

    if not candle:
        raise HTTPException(
        status_code= status.HTTP_404_NOT_FOUND,
        detail= "candle not found"
        )

    db.delete(candle)
    db.commit()

    return