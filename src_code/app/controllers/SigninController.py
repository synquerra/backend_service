from fastapi import Request
from app.models import get_db
from app.models.User import User
from passlib.context import CryptContext
from datetime import datetime, timedelta
from fastapi.responses import JSONResponse
from app.helpers.ErrorCodes import ErrorCodes
from app.helpers.JWTManager import JWTManager
from pydantic import BaseModel, EmailStr, Field
from app.helpers.ErrorMessages import ErrorMessages
from app.controllers.APIResponse import APIResponse
from app.helpers.ValidationHelper import ValidationHelper


# Helper: Current IST time
def now_ist():
    """Return current datetime in IST (UTC+5:30)."""
    return datetime.utcnow() + timedelta(hours=5, minutes=30)


# Signin Request Model (Pydantic v2 compatible)
class SigninRequest(BaseModel):
    email: str = Field(..., example="john@example.com")
    password: str = Field(..., min_length=8, max_length=256, example="StrongPassword123!")

    class Config:
        extra = "forbid"  # Prevent unexpected fields


# Signin Controller
class SigninController:
    def __init__(self):
        # Strong Argon2 configuration — same as Signup
        self.pwd_context = CryptContext(
            schemes=["argon2"],
            deprecated="auto",
            argon2__rounds=3,
            argon2__memory_cost=102400,
            argon2__parallelism=8
        )

    async def login_user(self, payload: SigninRequest, request: Request):
        """
        Authenticate user securely using Argon2, update last login IST timestamp,
        and return masked info with JWT tokens.
        """
        db = get_db()
        try:
            # Sanitize input
            email = payload.email.lower().strip()
            password = payload.password.strip()

            # Find user by email
            user = await db.find_one(User, {"EMAIL": email})
            if not user:
                return ValidationHelper.error_response(msg=ErrorMessages.LOGIN_FAILED, code=ErrorCodes.UNAUTHORIZED)

            # Verify password
            if not self.pwd_context.verify(password, user.PASSWORD):
                return ValidationHelper.error_response(msg=ErrorMessages.LOGIN_FAILED, code=ErrorCodes.UNAUTHORIZED)

            # Optional: Rehash if algorithm parameters changed
            if self.pwd_context.needs_update(user.PASSWORD):
                user.PASSWORD = self.pwd_context.hash(password)
                await db.save(user)

            # Check account status
            if getattr(user, "IS_ACTIVE", True) is False:
                return ValidationHelper.error_response(msg="User account is inactive. Please contact support.", code=ErrorCodes.UNAUTHORIZED)

            # Update LAST_LOGIN_AT, REGISTERED_IP, USER_AGENT
            user.LAST_LOGIN_AT = now_ist()
            user.REGISTERED_IP = request.client.host if request.client else "unknown"
            user.USER_AGENT = request.headers.get("user-agent", "unknown")
            await db.save(user)

            # Generate JWT tokens
            tokens = JWTManager.create_tokens(user.UNIQUE_ID, user.EMAIL)

            # Mask sensitive info
            masked_email = ValidationHelper.mask_email(user.EMAIL)
            masked_mobile = ValidationHelper.mask_mobile(user.MOBILE)

            # Return success response
            return JSONResponse(
                content=APIResponse.success(msg=ErrorMessages.LOGIN_SUCCESS, data={"unique_id": user.UNIQUE_ID, "first_name": user.FIRST_NAME, "middle_name": getattr(user, "MIDDLE_NAME", ""), "last_name": user.LAST_NAME, "email": masked_email, "mobile": masked_mobile, "tokens": tokens, "is_email_verified": getattr(user, "IS_EMAIL_VERIFIED", False), "is_mobile_verified": getattr(user, "IS_MOBILE_VERIFIED", False), "last_login_at": user.LAST_LOGIN_AT.strftime("%Y-%m-%d %H:%M:%S") if user.LAST_LOGIN_AT else None}), status_code=ErrorCodes.SUCCESS)

        except Exception as e:
            # Catch-all: log & return uniform error
            return ValidationHelper.error_response(msg=f"Unexpected error while signing in: {str(e)}", code=ErrorCodes.INTERNAL_SERVER_ERROR)
