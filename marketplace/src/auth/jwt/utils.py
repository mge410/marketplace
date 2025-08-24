from datetime import datetime, timedelta, timezone

import jwt

from src.auth.schemes.login_user import TokenPayload, TokenInfo
from src.core.config import settings
from src.core.database import UserModel

async def create_jwt_token(user: UserModel) -> TokenInfo:
    max_age = settings.auth_jwt.access_token_expire_minutes
    token = generate_token_info(user, settings.auth_jwt.access_token_expire_minutes)
    token_info = TokenInfo(
        token=token,
        token_type=settings.auth_jwt.token_type,
        max_age=max_age
    )
    return token_info

def generate_token_info(
        user: UserModel,
        expires_in: int,
) -> str:
    return encode_jwt_token(
        TokenPayload(
            sub=user.uuid,
            id=user.id,
            email=user.email,
            name=user.name,
            phone=user.phone,
            exp=expires_in,
        ),
    )

def encode_jwt_token(
        payload: TokenPayload,
        private_key: str = settings.auth_jwt.private_key_path.read_text(),
        algorithm: str = settings.auth_jwt.algorithm,
) -> str:
    payload = payload.model_dump()
    now = datetime.now(timezone.utc)
    payload["exp"] = now + timedelta(minutes=payload["exp"])
    payload["iat"] = now
    encoded = jwt.encode(payload, private_key, algorithm=algorithm)
    return encoded

def decode_jwt_token(
        token: str | bytes,
        public_key: str = settings.auth_jwt.public_key_path.read_text(),
        algorithm: str = settings.auth_jwt.algorithm,
):
    decode = jwt.decode(token, public_key, algorithms=algorithm)
    return decode
