import jwt
from schemas.auth_schemas import AccessSchema, RefreshSchema
from schemas.user_schemas import UserSchema
from datetime import datetime, timedelta
from api.config import Config
from fastapi import HTTPException

class AuthServices:
    def create_jwt(self, user: UserSchema):
        access_payload = {
            "sub": user.email,
            "exp": datetime.utcnow() + timedelta(seconds=config.EXP_ACCESS),
            "type": "access"
        }

        refresh_payload = {
            "sub": user.email,
            "exp": datetime.utcnow() + timedelta(seconds=config.EXP_REFRESH),
            "type": "refresh"
        }

        # Access Token
        access_token = jwt.encode(
            payload=access_payload,
            key=config.SECRET_KEY,
            algorithm=config.ALGORITHM
        )

        # Refresh Token
        refresh_token = jwt.encode(
            payload=refresh_payload,
            key=config.SECRET_KEY,
            algorithm=config.ALGORITHM
        )

        return {
            "access": access_token,
            "refresh": refresh_token
        }

    def verify_token(self, access_token: AccessSchema):
        try:
            payload = jwt.decode(
                jwt=access_token,
                key=config.SECRET_KEY,
                algorithms=[config.ALGORITHM]
            )
        
            if payload.get("type") != "access":
                raise HTTPException(
                    status_code=401,
                    detail="Token de tipo diferente!"
                )
            
            return payload

        except jwt.InvalidSignatureError:
            raise HTTPException(
                status_code=401,
                detail="Token inválido ou alterado!"
            )
        
        except jwt.ExpiredSignatureError:
            raise HTTPException(
                status_code=401,
                detail="Token expirado!"
            )

    def renovade_access_token(self, refresh_token: RefreshSchema):
        try:
            payload = jwt.decode(
                    jwt=refresh_token,
                    key=config.SECRET_KEY,
                    algorithms=[config.ALGORITHM]
                )
            
            if payload.get("type") != "refresh":
                raise HTTPException(
                    status_code=401,
                    detail="Token de tipo diferente!"
                )
            
            access_payload = {
                "sub": payload.get("sub"),
                "exp": datetime.utcnow() + timedelta(seconds=config.EXP_ACCESS),
                "type": "access"
            }

            new_access_token = jwt.encode(
                payload=access_payload,
                key=config.SECRET_KEY,
                algorithm=config.ALGORITHM
            )

            return {
                "access": new_access_token
            }
        
        except jwt.InvalidSignatureError:
            raise HTTPException(
                status_code=401,
                detail="Token inválido ou alterado!"
            )
        
        except jwt.ExpiredSignatureError:
            raise HTTPException(
                status_code=401,
                detail="Token expirado!"
            )