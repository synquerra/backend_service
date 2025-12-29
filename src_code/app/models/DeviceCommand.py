# app/models/DeviceCommand.py

from odmantic import Model
from datetime import datetime
from typing import Optional

class DeviceCommand(Model):
    imei: str
    command: str
    payload: dict
    qos: int
    status: str  # SENT, DELIVERED, EXECUTED, FAILED, TIMEOUT
    created_at: datetime = datetime.utcnow()
    updated_at: Optional[datetime] = None
