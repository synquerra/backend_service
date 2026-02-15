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
    student_name: Optional[str] = None
    student_id: Optional[str] = None

    model_config = {
        "collection": "devices_master"
    }
