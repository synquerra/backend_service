import uuid
from typing import Optional
from datetime import datetime
from datetime import timedelta
from odmantic import Model, Field
from app.helpers.CommonHelper import CommonHelper


def now_ist():
    """Return current IST datetime."""
    return datetime.utcnow() + timedelta(hours=5, minutes=30)


class User(Model):
    # Core Identity
    UNIQUE_ID: str = Field(default_factory=lambda: f"SQ_{uuid.uuid4()}", unique=True)
    FIRST_NAME: str
    MIDDLE_NAME: Optional[str] = ""
    LAST_NAME: str

    # Contact Info
    EMAIL: str = Field(..., unique=True)
    MOBILE: str = Field(..., unique=True)
    IMEI: str

    # Authentication
    PASSWORD: str
    PASSWORD_LAST_CHANGED_AT: Optional[datetime] = None
    PASSWORD_RESET_TOKEN: Optional[str] = None
    PASSWORD_RESET_EXPIRY: Optional[datetime] = None

    # Verification
    IS_EMAIL_VERIFIED: bool = False
    IS_MOBILE_VERIFIED: bool = False
    EMAIL_VERIFICATION_TOKEN: Optional[str] = None
    MOBILE_OTP: Optional[str] = None

    # Account Status
    IS_ACTIVE: bool = True
    FAILED_LOGIN_ATTEMPTS: int = 0

    # Metadata/Audit
    CREATED_AT: datetime = Field(default_factory=now_ist)
    UPDATED_AT: Optional[datetime] = None
    LAST_LOGIN_AT: Optional[datetime] = None
    REGISTERED_IP: Optional[str] = None
    USER_AGENT: Optional[str] = None

    # ODMantic Model Config
    model_config = {
        "collection": "sq_users"  # MongoDB collection name
    }
