from fastapi import APIRouter
from app.controllers.SignupController import SignupController, SignupRequest

router = APIRouter()
signup_controller = SignupController()

@router.post("/signup", summary="Register a new user")
async def signup(payload: SignupRequest):
    """
    Create a new user with:
    - UNIQUE_ID auto-generated
    - Unique EMAIL and MOBILE
    - Password hashed using Argon2
    """
    return await signup_controller.register_user(payload)
