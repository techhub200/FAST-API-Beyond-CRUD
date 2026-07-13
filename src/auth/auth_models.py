from sqlalchemy import Boolean, Column, DateTime, Integer, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class AuthUser(Base):
    __tablename__ = "auth_user"

    User_id = Column(Integer, primary_key=True)
    Username = Column(String, nullable=False, unique=True)
    Role = Column(String ,nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)
    is_verified = Column(Boolean, default=False)

