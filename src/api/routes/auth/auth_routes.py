from fastapi import APIRouter
from schemas.user_schemas import UserSchema
from services.auth_services import AuthServices
from services.user_services import UserServices
from fastapi import HTTPException, Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from typing import Annotated
from schemas.auth_schemas import RefreshSchema

router = APIRouter(tags=["Auth"], prefix="/auth")

auth = AuthServices()
user_services = UserServices()
bearer = HTTPBearer()

@router.post("/register")
async def user_auth_register(user: UserSchema):
    try:
        return user_services.add_user(
            user.email,
            user.senha
        )

    except Exception as e:
        raise HTTPException(
            status_code=401,
            detail="Esta conta já existe!"
        )

@router.post("/login")
async def user_auth_login(user: UserSchema):
    try:
        user_services.verify_user(
            user.email,
            user.senha
        )

        return auth.create_jwt(user)

    except Exception as e:
        raise HTTPException(
            status_code=401,
            detail=str(e)
        )
    
@router.post("/verify")
async def verify_access_token(access_token: Annotated[HTTPAuthorizationCredentials, Depends(bearer)]):
    return auth.verify_token(access_token.credentials)

@router.post("/refresh")
async def renovator_access_token(refresh_token: Annotated[HTTPAuthorizationCredentials, Depends(bearer)]):
    return auth.renovade_access_token(refresh_token.credentials)