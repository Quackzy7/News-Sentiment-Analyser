from fastapi import HTTPException,Request
from app.services.auth_service import verify_jwt_token

def get_current_user(request:Request)->dict:
    auth_header=request.headers.get("Authorization")

    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=401,detail="Not authenticated. Please login first.")
    token=auth_header.split(" ")[1]
    payload=verify_jwt_token(token)

    if not payload:
         raise HTTPException(
            status_code=401,
            detail="Invalid or expired token. Please login again."
        )
    
    return {
        "id": payload["sub"],
        "email": payload["email"],
        "name": payload["name"],
    }