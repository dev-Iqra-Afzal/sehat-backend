from fastcrud import FastCRUD

from ..db.token_blacklist import TokenBlacklist
from ..schemas import TokenBlackListCreate, TokenBlackListUpdate, TokenBlackListRead

CRUDTokenBlackList = FastCRUD[
    TokenBlacklist,
    TokenBlackListCreate,
    TokenBlackListUpdate,
    TokenBlackListUpdate,
    TokenBlackListUpdate,
    TokenBlackListRead
]

crud_token_blacklist = CRUDTokenBlackList(TokenBlacklist)
