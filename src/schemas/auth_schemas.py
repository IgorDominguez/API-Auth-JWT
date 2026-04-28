from pydantic import BaseModel

class AccessSchema(BaseModel):
    access_token: str

class RefreshSchema(BaseModel):
    refresh_token: str