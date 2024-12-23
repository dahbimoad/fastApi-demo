#this is : routes/user.py
from sqlalchemy.exc import IntegrityError
from fastapi import  Depends, HTTPException
from fastapi.routing import  APIRouter
from sqlalchemy.orm import Session
from starlette import status
from app.db.database import get_db
from app import schemas, models, oauth2
from app.oauth2 import get_current_user
from app.schemas import UserOut
from app.utils import hash_password

router = APIRouter(
    prefix="/users",
    tags=["Users :)"],
)

@router.post("/", response_model=schemas.UserOut, status_code=status.HTTP_201_CREATED)
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):

    # 1) Check if user already exists -- outside the try block
    existing_user = db.query(models.User).filter(models.User.email == user.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    try:
        # 2) Inside try, only do DB insertion code that might raise IntegrityError
        hashed_password = hash_password(user.password)
        new_user = models.User(email=user.email, password=hashed_password)
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
        print(f"Unexpected error: {type(e).__name__}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating user: {str(e)}"
        )

@router.get("/me", response_model=UserOut, status_code=status.HTTP_200_OK)
def get_me(current_user: UserOut = Depends(get_current_user)):
    return current_user

@router.get("/{id}",response_model=UserOut, status_code=status.HTTP_200_OK)
def get_post( id : int, db: Session = Depends(get_db),current_user: schemas.UserOut = Depends(
    oauth2.get_current_user)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


