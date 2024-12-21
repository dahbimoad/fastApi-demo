#this is : routes/auth.py
from fastapi import APIRouter, HTTPException
from fastapi.params import Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from starlette import status
import database
import models
import oauth2
import schemas
import utils

router = APIRouter(tags=['Authentication'])

@router.post('/login')
def login(user_credentials : OAuth2PasswordRequestForm = Depends(), db :Session  = Depends(database.get_db)):

    #{ the user_credebtials store data like this
    #   "username": "exemple",
    #  "password":"exemple"
    #}
    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Incorrect email or password')

    if not utils.verify_password(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail='Incorrect email or password')
    #create token

    access_token = oauth2.create_access_token(data={"email": user.email})
    return {"access_token": access_token, "token_type": "bearer"}
