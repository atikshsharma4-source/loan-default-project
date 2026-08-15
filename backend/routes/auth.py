from fastapi import APIRouter, HTTPException
router = APIRouter()
ALLOWED_EMAIL_DOMAIN = "@graphicera.com"
COMMON_PASSWORD = "Bank@123"
@router.post("/login")
def login(email: str, password: str):
    if not email.endswith(ALLOWED_EMAIL_DOMAIN):
        raise HTTPException(
            status_code=401,
            detail="Invalid employee email"
        )
    if password != COMMON_PASSWORD:
        raise HTTPException(
            status_code=401,
            detail="Invalid password"
        )
    return {
        "message": "Login successful",
        "email": email
    }