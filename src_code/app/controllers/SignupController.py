import uuid
from fastapi import Request
from app.models import get_db
from app.models.User import User
from passlib.context import CryptContext
from fastapi.responses import JSONResponse
from app.helpers.ErrorCodes import ErrorCodes
from app.controllers.APIResponse import APIResponse
from app.helpers.ErrorMessages import ErrorMessages
from app.helpers.ValidationHelper import ValidationHelper
from pydantic import BaseModel, EmailStr, Field, validator


class SignupRequest(BaseModel):
    first_name: str = Field(..., min_length=2, max_length=50, example="John")
    middle_name: str = Field("", max_length=50, example="M")
    last_name: str = Field(..., min_length=1, max_length=50, example="Doe")
    email: EmailStr = Field(..., example="john@example.com")
    mobile: str = Field(..., pattern=r"^[6-9]\d{9}$", example="9876543210")
    password: str = Field(..., min_length=8, max_length=256, example="StrongPassword123!")

    @validator("password")
    def password_strength(cls, password):
        """Validate password strength using helper."""
        if not ValidationHelper.validate_password_strength(password):
            raise ValueError("Password must include uppercase, lowercase, number, special character, and be ≥8 chars long.")
        return password


class SignupController:
    def __init__(self):
        # Argon2 — best available password hashing algorithm
        self.pwd_context = CryptContext(
            schemes=["argon2"],
            deprecated="auto",
            argon2__rounds=3,
            argon2__memory_cost=102400,
            argon2__parallelism=8,
        )

    async def register_user(self, payload: SignupRequest, request: Request):
        db = get_db()
        try:
            # Sanitize Input
            first_name = ValidationHelper.sanitize_name(payload.first_name)
            middle_name = ValidationHelper.sanitize_name(payload.middle_name)
            last_name = ValidationHelper.sanitize_name(payload.last_name)
            email = payload.email.lower().strip()
            mobile = payload.mobile.strip()

            # Check Duplicates
            existing_user = await db.find_one(
                User, {"$or": [{"EMAIL": email}, {"MOBILE": mobile}]}
            )
            if existing_user:
                if existing_user.EMAIL == email:
                    return ValidationHelper.error_response(ErrorMessages.EMAIL_EXIST, ErrorCodes.CONFLICT)
                return ValidationHelper.error_response(ErrorMessages.MOBILE_EXIST, ErrorCodes.CONFLICT)

            # Hash Password
            hashed_password = self.pwd_context.hash(payload.password)
            unique_id = f"SQ_{uuid.uuid4()}"

            # Capture Client Meta
            ip_address = request.client.host if request and request.client else "unknown"
            user_agent = request.headers.get("user-agent", "unknown")

            # Build User Object
            new_user = User(
                UNIQUE_ID=unique_id,
                FIRST_NAME=first_name,
                MIDDLE_NAME=middle_name,
                LAST_NAME=last_name,
                EMAIL=email,
                MOBILE=mobile,
                PASSWORD=hashed_password,
                IS_EMAIL_VERIFIED=False,
                IS_MOBILE_VERIFIED=False,
                EMAIL_VERIFICATION_TOKEN=str(uuid.uuid4()),
                MOBILE_OTP=None,
                IS_ACTIVE=True,
                FAILED_LOGIN_ATTEMPTS=0,
                UPDATED_AT=None,
                LAST_LOGIN_AT=None,
                REGISTERED_IP=ip_address,
                USER_AGENT=user_agent,
                PASSWORD_LAST_CHANGED_AT=None,
                PASSWORD_RESET_TOKEN=None,
                PASSWORD_RESET_EXPIRY=None
            )

            # Save User
            await db.save(new_user)

            # Prepare Masked Response
            masked_email = ValidationHelper.mask_email(new_user.EMAIL)
            masked_mobile = ValidationHelper.mask_mobile(new_user.MOBILE)

            # Return Response
            return JSONResponse(
                content=APIResponse.success(
                    msg=ErrorMessages.USER_REGISTERED_SUCCESS,
                    data={
                        "unique_id": new_user.UNIQUE_ID,
                        "first_name": new_user.FIRST_NAME,
                        "middle_name": new_user.MIDDLE_NAME,
                        "last_name": new_user.LAST_NAME,
                        "email": masked_email,
                        "mobile": masked_mobile,
                        "is_email_verified": new_user.IS_EMAIL_VERIFIED,
                        "is_mobile_verified": new_user.IS_MOBILE_VERIFIED,
                    },
                ),
                status_code=ErrorCodes.SUCCESS,
            )

        except Exception as e:
            return ValidationHelper.error_response(msg=f"Unexpected error while signing up: {str(e)}", code=ErrorCodes.INTERNAL_SERVER_ERROR)
