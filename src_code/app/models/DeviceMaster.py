from datetime import datetime
from odmantic import Model, Field

class DeviceMaster(Model):
    device_unique_id: str = Field(unique=True)
    student_unique_id: str
    parent_unique_id: str
    imei: str
    model: str
    firmware_version: str
    status: str
    assigned_date: datetime

    model_config = {
        "collection": "devices_master"
    }
