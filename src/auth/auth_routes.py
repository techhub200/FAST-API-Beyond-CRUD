from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.auth.Pydantic_schemas import UserCreateModel
from src.auth.Pydantic_schemas import UserLoginModel
from src.auth.Pydantic_schemas import RefreshTokenRequestModel, TokenResponseModel
from src.auth.service import User_Service
from datetime import timedelta

from src.auth.utils import create_access_token, create_refresh_token, decode_refresh_token
from src.auth.utils import verify_password
from src.db.database import get_db
from src.auth.dependencies import Access_Token_Bearer
from src.db.redis import add_access_token_to_blacklist
from src.auth.dependencies import get_current_user
from datetime import datetime


auth_router = APIRouter()
user_service = User_Service()
access_token_bearer = Access_Token_Bearer()


@auth_router.get("/me", response_model=UserCreateModel)
async def get_me(user=Depends(get_current_user)):
    return user

#REGISTER 
@auth_router.post("/Sign_Up", status_code=status.HTTP_201_CREATED)
async def Sign_Up(user_data: UserCreateModel, db: Session = Depends(get_db)):
    email = user_data.email
    if await user_service.User_exist(email, db):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User already exists")
    return await user_service.Create_User(user_data, db)


#LOGIN 
@auth_router.post("/Login", response_model=TokenResponseModel)
async def Login(User_data: UserLoginModel, db: Session = Depends(get_db)):
    email = User_data.email
    password = User_data.password

    current_user = await user_service.get_user_by_email(email, db)
    if not current_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    if not verify_password(password, current_user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    user_payload = {"user_id": current_user.User_id, "email": current_user.email}

    access_token = create_access_token(user_payload, timedelta(minutes=15))
    refresh_token = create_refresh_token(user_payload, timedelta(days=7))

    return {"access_token": access_token, "refresh_token": refresh_token}


#REFRESH TOKEN (stateless)
@auth_router.post("/Refresh", response_model=TokenResponseModel)
async def Refresh(data: RefreshTokenRequestModel):
    try:
        payload = decode_refresh_token(data.refresh_token)
    except Exception:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired refresh token")

    user_payload = payload.get("user")
    if not user_payload:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token")

    # rotate refresh token as well
    access_token = create_access_token(user_payload, expiry=timedelta(minutes=15))
    new_refresh_token = create_refresh_token(user_payload, expiry=timedelta(days=7))

    return {"access_token": access_token, "refresh_token": new_refresh_token}


#DELETE EXISTING USER
@auth_router.delete("/Delete_user/{user_id}")
async def Delete_user(user_id: int, db: Session = Depends(get_db)):
    return await user_service.Delete_user(user_id, db)


@auth_router.post("/logout")
async def logout(token_data=Depends(access_token_bearer), user=Depends(role_required("admin"))):

    payload = token_data["payload"]

    jti = payload["jti"]
    exp_dt = datetime.fromtimestamp(payload["exp"])

    add_access_token_to_blacklist(
        jti=jti,
        exp=exp_dt,
    )

    return {"message": "Logged out (access token revoked)"}







