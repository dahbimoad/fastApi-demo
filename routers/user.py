from sqlite3 import IntegrityError

from fastapi import  Depends, HTTPException
from fastapi.routing import  APIRouter
from sqlalchemy.orm import Session
from starlette import status
from database import get_db
import schemas
import models
from schemas import UserOut
from utils import hash_password

router = APIRouter(
    prefix="/users",
    tags=["Users :)"],
)

@router.post("/" ,response_model=schemas.UserOut , status_code=status.HTTP_201_CREATED)
def register(user: schemas.UserCreate ,db:Session = Depends(get_db)):
    try:
        # Check if user already exists
        existing_user = db.query(models.User).filter(models.User.email == user.email).first()
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )

        # Hash the password
        hashed_password = hash_password(user.password)

        # Create new user
        new_user = models.User(
            email=user.email,
            password=hashed_password
        )

        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        return new_user

    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating user: {str(e)}"
        )


@router.get("/{id}",response_model=UserOut, status_code=status.HTTP_200_OK)
def get_post( id : int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user