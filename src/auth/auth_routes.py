from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.auth.Pydantic_schemas import UserCreateModel
from src.auth.Pydantic_schemas import UserLoginModel
from src.auth.service import User_Service
from datetime import timedelta
from src.auth.utils import create_access_token
from src.auth.utils import decode_access_token
from src.auth.utils import verify_password
from src.db.database import get_db
from fastapi.security import OAuth2PasswordRequestForm
from src.auth.dependencies import Access_Token_Bearer


auth_router = APIRouter()
user_service = User_Service()
access_token_bearer = Access_Token_Bearer()


@auth_router.post("/Sign_Up", status_code=status.HTTP_201_CREATED)
async def Sign_Up(user_data: UserCreateModel, db: Session = Depends(get_db)):
    email = user_data.email
    if await user_service.User_exist(email, db):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User already exists")
    return await user_service.Create_User(user_data, db)
    

@auth_router.delete("/Delete_user/{user_id}")
async def Delete_user(user_id:int, db: Session = Depends(get_db)):
    
        return await user_service.Delete_user(user_id,db)

@auth_router.post("/Login")
async def Login(User_data: UserLoginModel, db: Session = Depends(get_db)):
     email = User_data.email
     password = User_data.password
     current_user = await user_service.get_user_by_email(email,db)
     if not current_user:
         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
     if not  verify_password(password, current_user.password):
          raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
     
     access_token= create_access_token({"user_id":current_user.User_id, "email":current_user.email},expiry=timedelta(minutes=15));
     return access_token