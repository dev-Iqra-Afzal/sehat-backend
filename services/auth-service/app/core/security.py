from pydantic import SecretStr
from enum import Enum
import bcrypt
from jose import jwt, JWTError
from fastapi.security import OAuth2PasswordBearer
from typing import Any, Literal
from datetime import timezone, datetime, timedelta
from sqlalchemy.ext.asyncio import AsyncSession

from .config import settings
from .schemas import TokenData, TokenBlackListCreate
from .db.crud_token_blacklist import crud_token_blacklist
from ..models.user import User
from ..crud.user import user_crud
from .redis_client import redis_client

SECRET_KEY: SecretStr = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES
REFRESH_TOKEN_EXPIRE_DAYS = settings.REFRESH_TOKEN_EXPIRE_DAYS

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

class TokenType(str, Enum):
    ACCESS = "access"
    REFRESH = "refresh"

# gensalt() generates a salt(some values), it makes sure that every same password have
async def get_password_hash(password: str)-> str:
    hashed_password: str = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    return hashed_password

# checkpw: is a function that checks the if password is correct by matching with its hashed version
# we are passing passwords through .encode() because it takes only in bytes format and we are receiving in string format
async def verify_password(plan_password: str, hashed_password: str)-> bool:
    is_correct: bool = bcrypt.checkpw(plan_password.encode(), hashed_password.encode())
    return is_correct

# jwt.encode() is used to create a JSON Web Token (JWT) from the given data and secret key
# It takes the data to encode, the secret key, and the algorithm to use for encoding
# data is a dictionary that contains the claims to be included in the JWT, such as user ID, roles, and expiration time
# when user will send its token for authentification, it will be decoded in "data" format to check if user is same to whom token was issued
async def create_access_token(data: dict[str, Any], expires_delta: timedelta | None = None) -> str:
    to_encode = data.copy()

    # datetime represents specific point in time, timedelta represents duration or difference between two dates (e.g., 1 day, 2 hours)
    if expires_delta:
        expire = datetime.now(timezone.utc).replace(tzinfo=None) + expires_delta
    else:
        expire = datetime.now(timezone.utc).replace(tzinfo=None) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire, "token_type": TokenType.ACCESS})
    encoded_jwt: str = jwt.encode(to_encode, SECRET_KEY.get_secret_value(), algorithm=ALGORITHM)
    return encoded_jwt

# create_refresh_token is similar to create_access_token, but it creates a refresh token with a longer expiration time
# The refresh token is used to obtain a new access token when the current one expires
async def create_refresh_token(data: dict[str, Any], expires_delta: timedelta | None = None) -> str:
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.now(timezone.utc).replace(tzinfo=None) + expires_delta
    else:
        expire = datetime.now(timezone.utc).replace(tzinfo=None) + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)

    to_encode.update({"exp": expire, "token_type": TokenType.REFRESH})
    encoded_jwt: str = jwt.encode(to_encode, SECRET_KEY.get_secret_value(), algorithm=ALGORITHM)
    return encoded_jwt


# async def verify_token(token: str, expected_token_type: TokenType, db: AsyncSession) -> TokenData | None:
    
#     is_blacklisted = await crud_token_blacklist.exists(db, token=token)
#     if is_blacklisted:
#         return None
    
#     try:
#         payload = jwt.decode(token, SECRET_KEY.get_secret_value(), algorithms=[ALGORITHM])
#         username_or_email: str = payload.get("sub")
#         token_type: str = payload.get("token_type")

#         if username_or_email is None or token_type != expected_token_type.value:
#             return None
        
#         return TokenData(username_or_email=username_or_email)
    
#     except JWTError:
#         return None

def is_token_blacklisted(token: str) -> bool:
    return redis_client.exists(token) == 1

async def verify_token(token: str, expected_token_type: TokenType) -> TokenData | None:
    if is_token_blacklisted(token):
        return None

    try:
        payload = jwt.decode(token, SECRET_KEY.get_secret_value(), algorithms=[ALGORITHM])
        username_or_email: str = payload.get("sub")
        token_type: str = payload.get("token_type")

        if username_or_email is None or token_type != expected_token_type.value:
            return None
        
        return TokenData(username_or_email=username_or_email)

    except JWTError:
        return None
    
async def blacklist_tokens(access_token: str, refresh_token: str) -> None:
    for token in [access_token, refresh_token]:
        payload = jwt.decode(token, SECRET_KEY.get_secret_value(), algorithms=[ALGORITHM])
        exp_timestamp = payload.get("exp")

        if exp_timestamp is not None:
            now = datetime.now(timezone.utc).timestamp()
            ttl = int(exp_timestamp - now)
            if ttl > 0:
                redis_client.setex(token, ttl, "blacklisted")

# async def blacklist_tokens(access_token: str, refresh_token: str, db: AsyncSession) -> None:

#     for token in [access_token, refresh_token]:
#         payload = jwt.decode(token, SECRET_KEY.get_secret_value(), algorithms=[ALGORITHM])
#         exp_timestamp = payload.get("exp")

#         if exp_timestamp is not None:
#             expires_at = datetime.fromtimestamp(exp_timestamp, tz=timezone.utc).astimezone(timezone.utc)
#             await crud_token_blacklist.create(db, object=TokenBlackListCreate(token=token, expires_at=expires_at))


async def blacklist_token(token: str, db: AsyncSession) -> None:
    payload = jwt.decode(token, SECRET_KEY.get_secret_value(), algorithms=[ALGORITHM])
    exp_timestamp = payload.get("exp")

    if exp_timestamp is not None:
        expires_at = datetime.fromtimestamp(exp_timestamp, tz=timezone.utc).astimezone(timezone.utc)
        await crud_token_blacklist.create(db, token=token, expires_at=expires_at)
    

async def authenticate_user(username_or_email: str, password: str, db: AsyncSession)-> User | Literal[False]:
    if "@" in username_or_email:
        db_user = await user_crud.get(db=db, email=username_or_email)

    else:
        db_user = await user_crud.get(db=db, username=username_or_email)

    if not db_user:
        return False
        
    if not await verify_password(password, db_user.password_hash):
        return False
        
    return db_user





