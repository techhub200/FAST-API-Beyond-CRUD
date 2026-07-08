from fastapi.security import HTTPBearer
from fastapi import HTTPException, Request
from fastapi.security.http import HTTPAuthorizationCredentials
from src.auth.utils import decode_access_token

class Access_Token_Bearer(HTTPBearer):
    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super().__call__(request)

        try:
            payload = decode_access_token(credentials.credentials)
            return payload
        except Exception:
            raise HTTPException(status_code=401, detail="Invalid or expired token")