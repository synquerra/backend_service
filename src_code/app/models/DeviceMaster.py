# app/models/DeviceMaster.py
from odmantic import Model, Field
from datetime import datetime, timedelta
from typing import Optional

def now_ist():
    return datetime.utcnow() + timedelta(hours=5, minutes=30)

class DeviceMaster(Model):
    topic: str
    imei: Optional[str] = None
    interval: Optional[int] = None
    Geoid: Optional[str] = None
    created_at: datetime = Field(default_factory=now_ist)

    model_config = {
        "collection": "devices_master"
    }
