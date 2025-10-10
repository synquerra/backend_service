import uuid
from datetime import datetime
from odmantic import Model, Field

class User(Model):
    UNIQUE_ID: str = Field(default_factory=lambda: f"SQ_{uuid.uuid4()}", unique=True)
    FIRST_NAME: str
    MIDDLE_NAME: str = ""
    LAST_NAME: str
    EMAIL: str = Field(..., unique=True)
    MOBILE: str = Field(..., unique=True)
    PASSWORD: str
    created_at: datetime = Field(default_factory=datetime.utcnow)

    # Use model_config instead of Config in Pydantic v2
    model_config = {
        "collection": "sq_users"  # MongoDB collection name
    }
