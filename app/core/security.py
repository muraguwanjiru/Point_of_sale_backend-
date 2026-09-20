import os
import hashlib
import secrets
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv
from fastapi import HTTPException, status
import jwt      

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM", "HS256")

if not SECRET_KEY:
    raise RuntimeError("CRITICAL ERROR: SECRET_KEY is missing from the environment variables (.env).")


def Hash_password(password: str) -> str:
    if not password or not password.strip():
        raise ValueError("Password cannot be empty.")
    
    # Generate a secure 16-byte random salt
    salt = secrets.token_bytes(16)
    
    # Hash using standard PBKDF2 with SHA-256 (highly secure, no library breaks)
    hash_bytes = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)
    
    # Store both salt and hash together as hex strings separated by a colon
    return f"{salt.hex()}:{hash_bytes.hex()}"


def Verify_password(plain_password: str, hashed_password: str) -> bool:
    if not plain_password or not hashed_password:
        return False
    try:
        # Split the salt and the original hash match
        salt_hex, original_hash_hex = hashed_password.split(":")
        salt = bytes.fromhex(salt_hex)
        
        # Hash the incoming password with the exact same salt
        new_hash = hashlib.pbkdf2_hmac('sha256', plain_password.encode('utf-8'), salt, 100000)
        
        # Use constant-time comparison to protect against timing attacks
        return secrets.compare_digest(new_hash.hex(), original_hash_hex)
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
