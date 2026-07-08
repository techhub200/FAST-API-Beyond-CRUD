from datetime import datetime

from sqlalchemy.orm import Session

from src.auth.Pydantic_schemas import UserCreateModel
from src.auth.auth_models import AuthUser
from src.auth.utils import generate_hashed_password


class User_Service:
    async def get_user_by_email(self, email: str, db: Session):
        return db.query(AuthUser).filter(AuthUser.email == email).first()

    async def User_exist(self, email: str, db: Session):
        return await self.get_user_by_email(email, db) is not None

    async def Create_User(self, user_data: UserCreateModel, db: Session):
        new_user = AuthUser(
            User_id=None,
            Username=user_data.username,
            email=user_data.email,
            password=generate_hashed_password(user_data.password),
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
            is_verified=False,
        )

        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return {
            "message": "User created successfully",
            "user": {
                "username": new_user.Username,
                "email": new_user.email,
            },
        }

    async def Delete_user(self, user_id: int, db: Session):
        user = db.query(AuthUser).filter(AuthUser.User_id == user_id).first()
        if not user:
            return {"message": "User not found"}
        else:
            db.delete(user)
            db.commit()
            return {"message": "User deleted successfully"}