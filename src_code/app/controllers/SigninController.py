from app.models import get_db
from app.models.User import User
from passlib.context import CryptContext
from fastapi.responses import JSONResponse
from app.helpers.ErrorCodes import ErrorCodes
from pydantic import BaseModel, EmailStr, Field
from app.helpers.ErrorMessages import ErrorMessages
from app.controllers.APIResponse import APIResponse
from app.helpers.ValidationHelper import ValidationHelper


# Signin Request Model (Pydantic v2 compatible)
class SigninRequest(BaseModel):
    email: EmailStr = Field(..., example="john@example.com")
    password: str = Field(..., min_length=8, max_length=256, example="StrongPassword123!")

    class Config:
        extra = "forbid"  # Prevent unexpected fields


# Signin Controller (Production Ready)
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

    async def login_user(self, payload: SigninRequest):
        """
        Authenticate user securely using Argon2.
        """
        db = get_db()
        try:
            # Normalize and sanitize inputs
            email = payload.email.lower().strip()
            password = payload.password.strip()

            # Find user by email
            user = await db.find_one(User, {"EMAIL": email})
            if not user:
                return ValidationHelper.error_response(msg=ErrorMessages.LOGIN_FAILED, code=ErrorCodes.UNAUTHORIZED)

            # Verify password
            if not self.pwd_context.verify(password, user.PASSWORD):
                return ValidationHelper.error_response(msg=ErrorMessages.LOGIN_FAILED, code=ErrorCodes.UNAUTHORIZED)

            # Optional: Rehash if algorithm parameters have changed
            if self.pwd_context.needs_update(user.PASSWORD):
                new_hash = self.pwd_context.hash(password)
                user.PASSWORD = new_hash
                await db.save(user)

            # Check if account is active
            if hasattr(user, "IS_ACTIVE") and not user.IS_ACTIVE:
                return ValidationHelper.error_response(msg="User account is inactive. Please contact support.", code=ErrorCodes.UNAUTHORIZED)

            # Return success response
            return JSONResponse(
                content=APIResponse.success(msg=ErrorMessages.LOGIN_SUCCESS,
                    data={"unique_id": user.UNIQUE_ID, "first_name": user.FIRST_NAME, "middle_name": getattr(user, "MIDDLE_NAME", ""), "last_name": user.LAST_NAME, "email": user.EMAIL, "mobile": user.MOBILE}), status_code=ErrorCodes.SUCCESS)

        except Exception as e:
            # Optionally integrate with Sentry or logger here
            return ValidationHelper.error_response(msg=f"Unexpected error while signing in: {str(e)}", code=ErrorCodes.INTERNAL_SERVER_ERROR)
