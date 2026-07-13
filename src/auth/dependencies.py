from fastapi.security import HTTPBearer
from fastapi import HTTPException, Request
from fastapi.security.http import HTTPAuthorizationCredentials
from src.auth.utils import decode_access_token



from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends

from src.db.database import get_db
from src.auth.service import User_Service


user_service = User_Service()


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


async def get_current_user(
    token_details: dict = Depends(Access_Token_Bearer()),
    session: AsyncSession = Depends(get_db),
):
    """Return current user based on access token payload."""
    user_payload = token_details["payload"].get("user")
    if not user_payload or not user_payload.get("email"):
        raise HTTPException(status_code=401, detail="Invalid token payload")

    user_email = user_payload["email"]
    user = await user_service.get_user_by_email(user_email, session)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


def role_required(required_role: str):
    """Dependency factory: allows access only for users with `required_role`."""

    async def _role_checker(user=Depends(get_current_user)):
        user_role = getattr(user, "Role", None)
        if user_role != required_role:
            raise HTTPException(status_code=403, detail="You are not allowed to perform this operation")
        return user

    return _role_checker

