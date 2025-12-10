from pydantic import BaseModel

class CommandModel(BaseModel):
    imei: str
