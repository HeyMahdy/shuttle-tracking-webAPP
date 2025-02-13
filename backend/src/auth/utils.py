import logging
import os
from datetime import timedelta, datetime

import jwt
from passlib.context import CryptContext
import uuid

from dotenv import load_dotenv
load_dotenv()



password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

ACCESS_TIME = 3600
def generate_password_hash(password:str):
    return password_context.hash(password)


def verify_password_hash(password:str, hash:str):
    return password_context.verify(password,hash)

logging.basicConfig(level=logging.INFO)

# Get environment variables
SECRET_KEY = os.environ.get("SECRET")
ALGORITHIM = os.environ.get("ALGORITHM")

# Log values (Caution: Do not log secret keys in production!)
logging.info(f"Using Algorithm: {ALGORITHIM}")
logging.info(f"Using Secret Key: {SECRET_KEY}****")


def create_access_token(data: dict , expiry : timedelta = None , refresh : bool = False):
    payload = {
    }
    payload["exp"] = datetime.now() + ( expiry if expiry is not None else  timedelta(seconds=ACCESS_TIME))
    payload["user"] = data
    payload["jti"] = str(uuid.uuid4())
    payload["refresh"] = refresh


    token = jwt.encode(
        payload = payload,
        key = SECRET_KEY,
        algorithm = ALGORITHIM

    )
    return token


def decode_token(token) -> dict:

    try:
        token_data = jwt.decode(
          jwt = token,
            key = SECRET_KEY,
            algorithms = [ALGORITHIM]
        )
        return token_data
    except jwt.PyJWTError as e:
        logging.exception(e , "this is going on")
















