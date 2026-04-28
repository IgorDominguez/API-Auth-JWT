from fastapi import APIRouter, Path
from services.auth_services import AuthServices
from services.user_services import UserServices
from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from typing import Annotated

router = APIRouter(tags=["User"], prefix="/user")

bearer = HTTPBearer()
auth = AuthServices()
user = UserServices()

@router.get("/profile")
async def user_profile(jwt: Annotated[HTTPAuthorizationCredentials, Depends(bearer)]):
    try:
        payload = auth.verify_token(jwt.credentials)

        return {
            "email": payload.get("sub")
        }
    except:
        raise HTTPException(
            status_code=401,
            detail="Seu token expirou!"
        )