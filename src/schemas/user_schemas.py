from pydantic import BaseModel

class UserSchema(BaseModel):
    email: str
    senha: str