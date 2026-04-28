from fastapi import APIRouter
from services.auth_services import AuthServices
from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from typing import Annotated

router = APIRouter(tags=["User"], prefix="/user")

bearer = HTTPBearer()
auth = AuthServices()

@router.get("/profile")
async def user_auth_login(jwt: Annotated[HTTPAuthorizationCredentials, Depends(bearer)]):
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