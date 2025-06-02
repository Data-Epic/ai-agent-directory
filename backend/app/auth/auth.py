import bcrypt
import jwt
import time
from datetime import datetime, timedelta
from dotenv import load_dotenv
import pytz
import os


load_dotenv()

nigeria_tz = pytz.timezone("Africa/Lagos")
SECRET_KEY = os.getenv("SECRET_KEY")
ACCESS_KEY_EXPIRATION_MINUTES = datetime.now(nigeria_tz) + timedelta(hours=24)
ALGORITHM = "HS256"


def hashed_password(password: str):
    hashed_password = bcrypt.hashpw(password.encode('utf-8'),
                        bcrypt.gensalt()).decode('utf-8')
    
    return hashed_password
                                                          
def verify_password(password: str,hashed_password: str):
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))

def generate_token(data:str) -> dict:
        id = data.get("id")
        expiration = ACCESS_KEY_EXPIRATION_MINUTES
        payload = {
            "sub": id,
            "exp": expiration,
        }

        return jwt.encode(payload,SECRET_KEY, algorithm=ALGORITHM)

def decodeJWT(token:str)-> dict:
    decode_token = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
    return decode_token if decode_token['exp'] >= time.time() else None
