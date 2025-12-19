from passlib.context import CryptContext
from datetime import timedelta, timezone, datetime
import jwt

from app.model_data import TokenData
from app.config import settings


crypto_context = CryptContext(schemes=["argon2"], deprecated="auto")


def get_passwd_hash(passwd: str) -> str:
    return crypto_context.hash(passwd)


def verify_passwd_hash(passwd: str, hash_passwd: str) -> bool:
    return crypto_context.verify(passwd, hash_passwd)


def create_access_token(
    data: TokenData,
    expires_delta: timedelta = timedelta(minutes=15),
) -> str:
    expire = datetime.now(timezone.utc) + expires_delta
    encode_data = {
        **data.model_dump(),
        "exp": expire,
    }
    encoded_jwt = jwt.encode(
        encode_data, settings.SECRET_KEY, algorithm=settings.JWT_HASH_ALGORITHM
    )
    return encoded_jwt


def verify_access_token(token: str) -> TokenData | None:
    try:
        user_data = jwt.decode(
            token, settings.SECRET_KEY, algorithms=settings.JWT_HASH_ALGORITHM
        )
    except jwt.ExpiredSignatureError:
        return None
    return TokenData.model_validate(user_data)
