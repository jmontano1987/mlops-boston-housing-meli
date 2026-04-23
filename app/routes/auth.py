from fastapi import APIRouter, HTTPException

from app.schemas.auth_schema import ClientCredentials
from app.security.auth import create_token, CLIENT_ID, CLIENT_SECRET

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/token")
def token(credentials: ClientCredentials):
    if credentials.client_id != CLIENT_ID or credentials.client_secret != CLIENT_SECRET:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = create_token({"sub": credentials.client_id})

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }
