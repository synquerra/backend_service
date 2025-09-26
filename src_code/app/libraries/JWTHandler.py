# Import Libraries
import jwt
from pathlib import Path
from typing import Dict

# Import custome libraries
from app.config.config import settings
from app.libraries.Logger import Logger

class JWTHandler:
    PRIVATE_KEY_PATH = Path(settings.UDISE_PRIVATE_KEY)
    PUBLIC_KEY_PATH = Path(settings.UDISE_PUBLIC_KEY)
    JWT_KID = settings.JWT_KID
    JWT_ALG = settings.JWT_ALG
    JWT_TYP = settings.JWT_TYP

    @classmethod
    def private_key(cls) -> str:
        if not cls.PRIVATE_KEY_PATH.exists():
            raise FileNotFoundError(f"Private key not found at {cls.PRIVATE_KEY_PATH}")
        key = cls.PRIVATE_KEY_PATH.read_text().strip()
        if not key:
            raise ValueError("Private key is empty or invalid")
        return key
        

    @classmethod
    def public_key(cls) -> str:
        if not cls.PUBLIC_KEY_PATH.exists():
            raise FileNotFoundError(f"Public key not found at {cls.PUBLIC_KEY_PATH}")
        key = cls.PUBLIC_KEY_PATH.read_text().strip()
        if not key:
            raise ValueError("Public key is empty or invalid")
        return key

    @classmethod
    def generate_token(cls, payload: Dict) -> tuple[bool, str]:
        logger = Logger.get_instance()
        try:
            private_key = cls.private_key()
            headers = {
                "kid": cls.JWT_KID,
                "alg": cls.JWT_ALG,
                "typ": cls.JWT_TYP
            }
            token = jwt.encode(payload, private_key, algorithm=cls.JWT_ALG, headers=headers)
            print(f"🔍 Debug: Generated JWT Token: {token}")
            return True, token
        except Exception as e:
            logger.log_critical(str(e))
            return False, str(e)
        
    @classmethod
    def decode_token(cls, token: str) -> tuple[bool, dict]:
        """Decodes JWT token using public key"""
        logger = Logger.get_instance()
        try:
            public_key = cls.public_key()
            payload = jwt.decode(token, public_key, algorithms=[cls.JWT_ALG])
            return True, payload
        except jwt.ExpiredSignatureError:
            return False, "Token has expired"
        except jwt.InvalidTokenError:
            return False, "Invalid token"
        except Exception as e:
            logger.log_critical(str(e))
            return False, str(e) 
           