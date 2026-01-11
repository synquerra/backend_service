from typing import Dict, Any
from pydantic import BaseModel, Field, validator, constr


class CommandRequest(BaseModel):
    imei: str = Field(..., min_length=15, max_length=15)
    command: constr(strip_whitespace=True, min_length=1)
    params: Dict[str, Any] = Field(default_factory=dict)

    @validator("imei")
    def validate_imei(cls, v):
        if not v.isdigit():
            raise ValueError("IMEI must be numeric")
        return v
