# app/models/CommandRequest.py

from pydantic import BaseModel, Field, validator

class CommandRequest(BaseModel):
    imei: str = Field(..., min_length=15, max_length=15)
    command: str
    params: dict = {}

    @validator("imei")
    def validate_imei(cls, v):
        if not v.isdigit():
            raise ValueError("IMEI must be numeric")
        return v
