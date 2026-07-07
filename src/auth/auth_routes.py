from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.auth.Validation_schemas import UserCreateModel
from src.auth.service import User_Service
from src.db.database import get_db


auth_router = APIRouter()
user_service = User_Service()


@auth_router.post("/Sign_Up", status_code=status.HTTP_201_CREATED)
async def Sign_Up(User_Data: UserCreateModel, db: Session = Depends(get_db)):
    email = User_Data.email
    user_exist = await user_service.User_exist(email, db)
    if user_exist:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User already exists")
    return await user_service.Create_User(User_Data, db)
    