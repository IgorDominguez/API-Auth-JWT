from database.connection import Session, Base, engine
from schemas.user_schemas import UserSchema
from database.models import User
from fastapi import HTTPException

Base.metadata.create_all(engine)

class UserServices:
    def __init__(self):
        self.session = Session()

    def add_user(self, email: str, senha: str):
        try:
            user = User(
                email=email,
                senha=senha
            )

            self.session.add(user)
            self.session.commit()
            self.session.refresh(user)

            return {
                "email": user.email,
                "senha": user.senha
            }

        except Exception as e:
            self.session.rollback()
            
            raise HTTPException(
                status_code=400,
                detail=e
            )
        finally:
            self.session.close()

    def verify_user(self, email: str, senha: str):
        try:
            user = self.session.query(User).filter_by(email=email).first()

            if not user or user.senha != senha:
                raise HTTPException(
                    status_code=401,
                    detail="Email ou senha incorretos!"
                )

            return {
                "email": user.email,
                "senha": user.senha
            }

        except HTTPException as http_exc:
            raise http_exc

        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Erro interno no servidor: {str(e)}"
            )
        finally:
            self.session.close()