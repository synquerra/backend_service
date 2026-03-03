from fastapi import APIRouter, Request
from app.controllers.SigninController import SigninController, SigninRequest

router = APIRouter()
signin_controller = SigninController()

@router.post("/signin")
async def signin_user(payload: SigninRequest, request: Request):
    return await signin_controller.login_user(payload, request)
