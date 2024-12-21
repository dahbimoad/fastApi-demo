from fastapi import APIRouter, HTTPException
from fastapi.params import Depends
from sqlalchemy.orm import Session
from starlette import status

import database
import models
import schemas
import utils

router = APIRouter(tags=['Authentication'])

@router.post('/login')
def login(user_credentials : schemas.UserLogin, db :Session  = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.email == user_credentials.email).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Incorrect email or password')

    if not utils.verify_password(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,)
    #create token
    return {"token " : "examplellllllllllllll"}