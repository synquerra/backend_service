import re
from fastapi.responses import JSONResponse
from app.controllers.APIResponse import APIResponse


class ValidationHelper:
    """
    Helper utilities for validation, sanitization, and standard error responses.
    """

    # ----------------------------------------------------
    # ✅ Password Strength Validator
    # ----------------------------------------------------
    @staticmethod
    def validate_password_strength(password: str) -> bool:
        """
        Checks password complexity — must contain:
        uppercase, lowercase, number, special character, and be at least 8 chars long.
        """
        if not password:
            return False
        if (
            len(password) < 8
            or not re.search(r"[A-Z]", password)
            or not re.search(r"[a-z]", password)
            or not re.search(r"\d", password)
            or not re.search(r"[@$!%*?&]", password)
        ):
            return False
        return True

    # ----------------------------------------------------
    # ✅ Helper: Sanitize Input
    # ----------------------------------------------------
    @staticmethod
    def sanitize_name(name: str) -> str:
        """
        Removes unwanted characters and normalizes capitalization.
        Example: '  jOhN! ' -> 'John'
        """
        if not name:
            return ""
        return re.sub(r"[^a-zA-Z\s]", "", name.strip().title())

    # ----------------------------------------------------
    # ✅ Helper: Uniform Error Responses
    # ----------------------------------------------------
    @staticmethod
    def error_response(msg: str, code: int):
        """
        Generates a standardized JSON error response using APIResponse format.
        """
        return JSONResponse(content=APIResponse.error(msg=msg, code=code), status_code=code)
