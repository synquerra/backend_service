import re
from html import escape
from fastapi.responses import JSONResponse
from app.controllers.APIResponse import APIResponse


class ValidationHelper:
    """Centralized validation and sanitization helper for defensive coding."""

    # Strong password validator
    @staticmethod
    def validate_password_strength(password: str) -> bool:
        """
        Checks if a password contains:
        - at least 1 uppercase
        - at least 1 lowercase
        - at least 1 number
        - at least 1 special character
        - length >= 8
        """
        pattern = (
            r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)"
            r"(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$"
        )
        return bool(re.match(pattern, password))

    # Sanitize user input to prevent script injection
    @staticmethod
    def sanitize_name(name: str) -> str:
        """
        Escapes HTML and trims whitespace for safe name inputs.
        Example: "<John>" → "&lt;John&gt;"
        """
        if not name:
            return ""
        return escape(name.strip())

    # Uniform error response helper
    @staticmethod
    def error_response(msg: str, code: int):
        """Standardized API error response."""
        return JSONResponse(content=APIResponse.error(msg=msg, code=code), status_code=code)

    # Mask email for privacy in responses
    @staticmethod
    def mask_email(email: str) -> str:
        """
        Masks part of the email before returning it in responses.
        Example: john.doe@example.com → jo***@example.com
        """
        try:
            local, domain = email.split("@")
            if len(local) <= 2:
                masked_local = local[0] + "***"
            else:
                masked_local = local[:2] + "***"
            return f"{masked_local}@{domain}"
        except Exception:
            return "***@***"

    # Mask mobile number for privacy
    @staticmethod
    def mask_mobile(mobile: str) -> str:
        """
        Example: 9876543210 → 98*****210
        """
        if not mobile or len(mobile) < 4:
            return "****"
        return f"{mobile[:2]}*****{mobile[-3:]}"
