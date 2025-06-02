import os
from datetime import datetime, timedelta

import bcrypt
import jwt
import pytz
from dotenv import load_dotenv

load_dotenv()

nigeria_tz = pytz.timezone("Africa/Lagos")
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"


def hashed_password(password: str):
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode(
        "utf-8"
    )


def verify_password(password: str, hashed: str):
    return bcrypt.checkpw(password.encode("utf-8"), hashed.encode("utf-8"))


def generate_token(data: dict) -> str:
    expiration = datetime.now(nigeria_tz) + timedelta(hours=24)
    payload = {
        "sub": data.get("id"),
        "exp": expiration,
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def decodeJWT(token: str) -> dict:
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except jwt.ExpiredSignatureError:
        return None
    except jwt.JWTError:
        return None
