from fastapi import APIRouter, Header
from app.config.config import settings
from app.helpers.JwtHandler import JWTHandler


# Create the APIRouter instance
router = APIRouter()

# Initialize the JWTHandler
jwt_handler = JWTHandler(secret_key=settings.JWT_SECRET_KEY,algorithm=settings.JWT_ALGORITHM,token_expiry_minutes=settings.JWT_TOKEN_EXPIRE_MINUTES)

@router.post("/generate-token/")
async def generate_token(username: str):
    """
    Generate a JWT token for a specific username.
    :param username: The username for which the token will be generated
    :return: JSONResponse containing the generated token
    """
    
    return jwt_handler.generate_token(username=username)

@router.get("/validate-token/")
async def validate_token(token: str = Header(...)):
    """
    Validate the provided JWT token.
    :param token: The JWT token to validate
    :return: JSONResponse indicating the validation result
    """
    return jwt_handler.validate_token(token=token)
