from fastapi import Request, HTTPException
from ..utils.security import verify_token

def auth_middleware(request: Request):
    token = request.headers.get("Authorization")
    if not token or not token.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    token = token.split(" ")[1]
    
    try:
        decoded = verify_token(token)
        request.state.user = decoded
    except Exception as e:
        raise HTTPException(status_code=401, detail="Invalid token")
