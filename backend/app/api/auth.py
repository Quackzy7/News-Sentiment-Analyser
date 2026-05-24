from fastapi import APIRouter,HTTPException,Request
from fastapi.responses import RedirectResponse
import httpx
import os
from dotenv import load_dotenv
from app.services.auth_service import create_jwt_token
from app.models.user import User
from app.services.auth_service import verify_jwt_token

load_dotenv()

router=APIRouter()

GOOGLE_CLIENT_ID=os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET=os.getenv("GOOGLE_CLIENT_SECRET")
FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:5173")
BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")

REDIRECT_URI = f"{BACKEND_URL}/api/v1/auth/callback"

GOOGLE_AUTH_URL = "https://accounts.google.com/o/oauth2/v2/auth"
GOOGLE_TOKEN_URL = "https://oauth2.googleapis.com/token"
GOOGLE_USERINFO_URL = "https://www.googleapis.com/oauth2/v3/userinfo"

@router.get("/login")
def login():
    params={
        "client_id":GOOGLE_CLIENT_ID,
        "redirect_uri":REDIRECT_URI,
        "response_type":"code",
        "scope":"openid email profile",
        "access_type":"offline",
    }
    query="&".join(f"{k}={v}" for k,v in params.items())
    return RedirectResponse(url=f"{GOOGLE_AUTH_URL}?{query}")

@router.get("/callback")
async def callback(code:str):
    async with httpx.AsyncClient() as client:
        token_reponse=await client.post(
            GOOGLE_TOKEN_URL,
            data={
                "code": code,
                "client_id": GOOGLE_CLIENT_ID,
                "client_secret": GOOGLE_CLIENT_SECRET,
                "redirect_uri":REDIRECT_URI,
                "grant_type": "authorization_code"
            }
        )

        if(token_reponse.status_code !=200):
            raise HTTPException(status_code=400,detail="Failed to get token from Google")

        tokens=token_reponse.json()
        access_token=tokens.get("access_token")

        userinfo_response=await client.get(
            GOOGLE_USERINFO_URL,
            headers={"Authorization": f"Bearer {access_token}"}
        )

        if userinfo_response.status_code!=200:
            raise HTTPException(status_code=400,detail="Failed to get user info from Google")
        
        userinfo=userinfo_response.json()

        user_data={
            "id":userinfo["sub"],
            "email": userinfo["email"],
            "name": userinfo.get("name",""),
            "picture": userinfo.get("picture","")
        }

        jwt_token=create_jwt_token(user_data)

        return RedirectResponse(
            url=f"{FRONTEND_URL}?token={jwt_token}"
        )
    

@router.get("/me", response_model=User)
async def get_me(request:Request):

    auth_header=request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=401,detail="Not authenticated")

    token=auth_header.split(" ")[1]
    payload=verify_jwt_token(token)

    if not payload: 
        raise HTTPException(status_code=401,detail="Invalid or expired token")

    return User(
        id=payload["sub"],
        email=payload["email"],
        name=payload["name"],
        picture=payload.get("picture")
    )