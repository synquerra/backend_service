import jwt
from fastapi.responses import JSONResponse
from app.helpers.ErrorCodes import ErrorCodes
from datetime import datetime, timedelta, timezone
from app.helpers.ErrorMessages import ErrorMessages
from app.controllers.APIResponse import APIResponse

class JWTHandler:
    def __init__(self, secret_key: str, algorithm: str, token_expiry_minutes: int):
        """Initialize with a secret key, algorithm, and token expiry time."""
        self.secret_key = secret_key
        self.algorithm = algorithm
        self.token_expiry_minutes = token_expiry_minutes

    def generate_token(self, username: str) -> JSONResponse:
        """Generate a JWT access token."""
        try:
            expire = datetime.now(timezone.utc) + timedelta(minutes=self.token_expiry_minutes)
            payload = {"sub": username, "exp": expire}
            token = jwt.encode(payload, self.secret_key, algorithm=self.algorithm)
            return JSONResponse(content=APIResponse.success(msg="Token generated successfully.", code=ErrorCodes.SUCCESS, data= {"access_token": token, "token_type": "bearer"},),status_code=ErrorCodes.SUCCESS)
        except Exception as e:
            return JSONResponse(content=APIResponse.success(msg=f"Failed to generate token: {str(e)}", code=ErrorCodes.INTERNAL_SERVER_ERROR,),status_code=ErrorCodes.INTERNAL_SERVER_ERROR)
            
    def validate_token(self, token: str) -> JSONResponse:
        """Validate and decode the JWT token."""
        try:
            decoded = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            return JSONResponse(content=APIResponse.success(msg="Token is valid.", code=ErrorCodes.SUCCESS, data= decoded),status_code=ErrorCodes.SUCCESS)
            
        except jwt.ExpiredSignatureError:
            return JSONResponse(content=APIResponse.success(msg=ErrorMessages.JWT_TOKEN_EXPIRED, code=ErrorCodes.UNAUTHORIZED,),status_code=ErrorCodes.UNAUTHORIZED)
            
        except jwt.InvalidTokenError:
            return JSONResponse(content=APIResponse.success(msg=ErrorMessages.INVALID_JWT_TOKEN, code=ErrorCodes.UNAUTHORIZED,),status_code=ErrorCodes.UNAUTHORIZED)
            