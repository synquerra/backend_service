from fastapi import Request
from app.controllers.SignupController import SignupController, SignupRequest

signup_controller = SignupController()

async def signup_user(payload: SignupRequest, request: Request):
    return await signup_controller.register_user(payload, request)
