from datetime import datetime

from sqlalchemy.orm import Session

from src.auth.Validation_schemas import UserCreateModel
from src.auth.auth_models import AuthUser
from src.auth.utils import generate_hashed_password


class User_Service:
    async def get_user_by_email(self, email: str, db: Session):
        user = db.query(AuthUser).filter(AuthUser.email == email).first()
        if not user:
            return None
        return user

    async def User_exist(self, email: str, db: Session):
        get_user = await self.get_user_by_email(email=email, db=db)
        if get_user:
            return True
        return False

    async def Create_User(self, User_data: UserCreateModel, db: Session):
        new_user = AuthUser(
            Username=User_data.username,
            email=User_data.email,
            password=generate_hashed_password(User_data.Password),
            First_name="",
            Last_name="",
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
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

