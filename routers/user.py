
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
       # hash the password
        user.password = hash_password(user.password)
        new_user = models.User(**user.dict())
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user


@router.get("/{id}",response_model=UserOut, status_code=status.HTTP_200_OK)
def get_post( id : int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user