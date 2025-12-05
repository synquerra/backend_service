# app/models/DeviceMaster.py
from odmantic import Model
from typing import Optional
from datetime import datetime


class DeviceMaster(Model):
    topic: str
    imei: Optional[str] = None
    interval: Optional[int] = None
    Geoid: Optional[str] = None
    created_at: Optional[datetime] = None

    model_config = {
        "collection": "devices_master"
    }
