from fastapi.security import HTTPBearer
from fastapi import HTTPException, Request
from fastapi.security.http import HTTPAuthorizationCredentials

from src.auth.utils import decode_access_token


class Access_Token_Bearer(HTTPBearer):
    def __init__(self):
        # Ensure FastAPI doesn't auto-return 403/401 before we can log details.
        super().__init__(auto_error=False)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials | None = await super().__call__(request)
        if credentials is None or not credentials.credentials:
            # Header missing or not in Bearer format.
            print("[Auth] Missing/invalid Authorization header (expected: Bearer <token>)", flush=True)
            raise HTTPException(status_code=401, detail="Invalid or expired token")

        token_str = credentials.credentials
        try:
            payload = decode_access_token(token_str)
            return {"token": token_str, "payload": payload}
        except Exception as e:
            # decode_access_token is responsible for logging exact jwt errors.
            print(f"[Auth] decode_access_token failed: {type(e).__name__}: {e}", flush=True)
            raise HTTPException(status_code=401, detail="Invalid or expired token")


