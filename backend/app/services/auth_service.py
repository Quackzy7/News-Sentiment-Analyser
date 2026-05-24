from jose import JWTError,jwt
from datetime import datetime,timedelta
import os
from dotenv import load_dotenv

load_dotenv()

JWT_SECRET=os.getenv("JWT_SECRET")
JWT_ALGORITHM="HS256"
JWT_EXPIRY_HOURS=24

def create_jwt_token(user_data:dict)->str:
    payload={
        "sub":user_data["id"],
        "email": user_data["email"],
        "name": user_data["name"],
        "picture": user_data.get("picture"),
        "exp": datetime.utcnow() + timedelta(hours=JWT_EXPIRY_HOURS)
    }
    return jwt.encode(payload,JWT_SECRET,algorithm=JWT_ALGORITHM)

def verify_jwt_token(token:str)->dict:
    try:
        payload=jwt.decode(token,JWT_SECRET,algorithms=[JWT_ALGORITHM])
        return payload 
    except JWTError:
        return None