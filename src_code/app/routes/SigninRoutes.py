from fastapi import Request
from app.controllers.SigninController import SigninController, SigninRequest

signin_controller = SigninController()

async def signin_user(payload: SigninRequest, request: Request):
    return await signin_controller.login_user(payload, request)
