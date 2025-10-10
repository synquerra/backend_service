import jwt
from app.config.config import settings
from datetime import datetime, timedelta
from fastapi.responses import JSONResponse
from app.helpers.ErrorCodes import ErrorCodes
from app.controllers.APIResponse import APIResponse
from app.helpers.ValidationHelper import ValidationHelper


class JWTManager:
    """
    Handles JWT generation and verification (Access + Refresh).
    """

    @staticmethod
    def create_tokens(user_id: str, email: str):
        """
        Generates access and refresh JWTs.
        """
        now = datetime.utcnow()
        access_exp = now + timedelta(minutes=int(settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES))
        refresh_exp = now + timedelta(days=int(settings.JWT_REFRESH_TOKEN_EXPIRE_DAYS))

        payload_access = {
            "sub": user_id,
            "email": email,
            "type": "access",
            "iat": now,
            "exp": access_exp
        }
        payload_refresh = {
            "sub": user_id,
            "email": email,
            "type": "refresh",
            "iat": now,
            "exp": refresh_exp
        }

        access_token = jwt.encode(payload_access, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
        refresh_token = jwt.encode(payload_refresh, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
            "expires_in": int(settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES) * 60
        }

    @staticmethod
    def verify_token(token: str, expected_type: str = "access"):
        """
        Verifies JWT and ensures correct token type (access/refresh).
        """
        try:
            decoded = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
            if decoded.get("type") != expected_type:
                raise jwt.InvalidTokenError("Invalid token type")
            return decoded
        except jwt.ExpiredSignatureError:
            return ValidationHelper.error_response("Token has expired", ErrorCodes.UNAUTHORIZED)
        except jwt.InvalidTokenError as e:
            return ValidationHelper.error_response(f"Invalid token: {str(e)}", ErrorCodes.UNAUTHORIZED)
