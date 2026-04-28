from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()

class Config(BaseSettings):
    SECRET_KEY: str
    EXP_ACCESS: int
    EXP_REFRESH: int
    ALGORITHM: str

config = Config()