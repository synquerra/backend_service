from fastapi import APIRouter, Request
from app.controllers.SigninController import SigninController, SigninRequest

router = APIRouter()
signin_controller = SigninController()

@router.post("/signin", summary="Login user")
async def signin(payload: SigninRequest, request: Request):
    """
    Login a user using email and password.
    Password is verified with Argon2 hashing.
    """
    return await signin_controller.login_user(payload, request)
