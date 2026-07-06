from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String ,DateTime,Boolean

Base=declarative_base()

class AuthUser(Base):
    __tablename__="auth_user"
    user_id=Column(Integer,primary_key=True)
    username=Column(String,nullable=False,unique=True)
    email=Column(String,nullable=False,unique=True)
    First_name=Column(String,nullable=False)
    Last_name=Column(String,nullable=False)
    created_at=Column(DateTime,nullable=False)
    updated_at=Column(DateTime,nullable=False)
    is_verified=Column(Boolean,default=False)

