import os
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv
from fastapi import HTTPException, status
import jwt      
import passlib.hash as passlib_hash

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM", "HS256")

if not SECRET_KEY:
    raise RuntimeError("CRITICAL ERROR: SECRET_KEY is missing from the environment variables (.env).")

def Hash_password(password: str) -> str:
    if not password or not password.strip():
        raise ValueError("Password cannot be empty.")
    return passlib_hash.recommended.hash(password)


def Verify_password(plain_password: str, hashed_password: str) -> bool:
    if not plain_password or not hashed_password:
        return False
    try:
        return passlib_hash.recommended.verify(plain_password, hashed_password)
    except Exception:
        return False


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    if not data or "sub" not in data:
        raise ValueError("Token data must contain a 'sub' claim identifier.")
        
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
        
    to_encode.update({
        "exp": expire,
        "iat": datetime.now(timezone.utc).timestamp(),
        "type": "access"
    })
    
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def decode_access_token(token: str):
    if not token or not token.strip():
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token missing",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
    try:
        payload: dict[str, any] = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        
        sub: str = payload.get("sub")
        if not sub or not str(sub).strip():
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token is missing user identifier (sub claim)",
                headers={"WWW-Authenticate": "Bearer"},
            )
            
        token_type = payload.get("type")
        if token_type and token_type != "access":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token scope",
                headers={"WWW-Authenticate": "Bearer"},
            )
            
        iat = payload.get("iat")
        if iat and datetime.now(timezone.utc).timestamp() < iat:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token issued in the future",
                headers={"WWW-Authenticate": "Bearer"},
            )

        return payload
        
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token signature or payload",
            headers={"WWW-Authenticate": "Bearer"},
        )
