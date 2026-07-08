from passlib.context import CryptContext
from datetime import timedelta, datetime
from src.config import JWT_SECRET, JWT_ALGORITHM
import jwt
password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def generate_hashed_password(password:str):
    return password_context.hash(password)

def verify_password(plain_password:str,hashed_password:str):
    return password_context.verify(plain_password,hashed_password)

def create_access_token(user_data: dict, expiry:timedelta):
    payload={
        "user":user_data,
        "exp":datetime.utcnow()+expiry,
    }

    token=jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
    return token
    
def decode_access_token(token:str):
    try:
        token_data=jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return token_data
    except jwt.pyjwt.exceptions.ExpiredSignatureError:
        raise Exception("Token has expired")  