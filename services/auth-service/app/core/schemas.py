from pydantic import BaseModel
from datetime import datetime



#-------------------- Token Schemas --------------------
class Token(BaseModel):
    access_token: str
    token_type: str 

class TokenData(BaseModel):
    username_or_email: str

class TokenBlackListBase(BaseModel):
    token: str
    expires_at: datetime

class TokenBlackListRead(TokenBlackListBase):
    id: int

class TokenBlackListCreate(TokenBlackListBase):
    pass

class TokenBlackListUpdate(TokenBlackListBase):
    pass