from fastapi import APIRouter, HTTPException, status
from sqlalchemy import select
import models
from schemas import UserPublicCreate, UserPublicResponse, UserUpdate
from dependencies import DbSession


router = APIRouter()


# ---- Create a new public user ----

@router.post("", response_model=UserPublicResponse,status_code=status.HTTP_201_CREATED,)
def register_public_user(user_in: UserPublicCreate, db: DbSession):
    result = db.execute(
        select(models.User).where(models.User.username == user_in.username)
    )
    existing_user = result.scalars().first()

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail= "User already exists"
        )
    
    result = db.execute(
        select(models.User).where(models.User.email == user_in.email)
    )
    existing_email = result.scalars().first()

    if existing_email:
        raise HTTPException(
            status_code= status.HTTP_400_BAD_REQUEST,
            detail= "Email already exists"
        )
    
    new_public_user = models.User(
        username = user_in.username,
        email = user_in.email
    )

    db.add(new_public_user)
    db.commit()
    db.refresh(new_public_user)

    return new_public_user


# ---- Get a public user ----

@router.get("/{user_id}", response_model=UserPublicResponse)
def get_user(user_id: int, db: DbSession):
    result = db.execute(
        select(models.User).where(models.User.id == user_id)
    )
    user = result.scalars().first()

    if user:
        return user
    
    raise HTTPException(
        status_code= status.HTTP_404_NOT_FOUND,
        detail= "User not found"
    )


# ---- Get a list for the public users ----

@router.get("", response_model=list[UserPublicResponse])
def get_all_users(db: DbSession):
    result = db.execute(
        select(models.User)
    )

    users= result.scalars().all()

    return users


# ---- User Update ----

@router.patch("/{user_id}", response_model=UserPublicResponse)
def update_user(
    user_id:int, 
    user_update:UserUpdate, 
    db:DbSession
    ):

    result = db.execute(select(models.User).where(models.User.id == user_id))
    user = result.scalars().first()

    if not user:
        raise HTTPException(
        status_code= status.HTTP_404_NOT_FOUND,
        detail= "User not found"
        )

    if user_update.username is not None and user_update.username != user.username:
        result = db.execute(select(models.User).where(models.User.username == user_update.username))

        existing_user= result.scalars().first()

        if existing_user:
            raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail= "Username already exists"
        )
    
    if user_update.email is not None and user_update.email != user.email:
        result = db.execute(
            select(models.User).where(models.User.email == user_update.email)
        )

        existing_email= result.scalars().first()

        if existing_email:
            raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail= "Email already registered"
        )
    
    update_data = user_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(user,field,value)
    
    db.commit()
    db.refresh(user)

    return user


# ---- Delete a user ----

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int, db: DbSession):
    result = db.execute(select(models.User).where(models.User.id == user_id))
    user = result.scalars().first()

    if not user:
        raise HTTPException(
        status_code= status.HTTP_404_NOT_FOUND,
        detail= "User not found"
        )

    db.delete(user)
    db.commit()

    return




