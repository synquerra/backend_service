from fastapi import APIRouter
from app.controllers.SigninController import SigninController, SigninRequest

router = APIRouter()
signin_controller = SigninController()

@router.post("/signin", summary="Login user")
async def signin(payload: SigninRequest):
    """
    Login a user using email and password.
    Password is verified with Argon2 hashing.
    """
    return await signin_controller.login_user(payload)
