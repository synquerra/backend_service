from odmantic import Model, Field
from typing import Optional
from datetime import datetime


class AnalyticsData(Model):
    # Primary fields
    topic: Optional[str] = None
    imei: Optional[str] = None
    interval: Optional[int] = None
    Geoid: Optional[str] = None

    # Packet info
    packet: Optional[str] = None
    Alert: Optional[str] = None
    type: Optional[str] = None

    # Telemetry
    latitude: Optional[str] = None
    longitude: Optional[str] = None
    speed: Optional[int] = None
    Battery: Optional[str] = None
    Signal: Optional[str] = None

    # NEW CLEAN TIMESTAMPS
    device_raw_timestamp: Optional[str] = None   # exact from device
    device_timestamp: Optional[datetime] = None       # IST converted

    # RAW (flattened) fields that still exist in DB
    raw_packet: Optional[str] = None
    raw_imei: Optional[str] = None
    raw_Alert: Optional[str] = None
    raw_temperature: Optional[str] = None
    raw_body: Optional[str] = None
    raw_phonenum1: Optional[str] = None
    raw_phonenum2: Optional[str] = None
    raw_controlroomnum: Optional[str] = None
    raw_NormalSendingInterval: Optional[str] = None
    raw_SOSSendingInterval: Optional[str] = None
    raw_NormalScanningInterval: Optional[str] = None
    raw_AirplaneInterval: Optional[str] = None
    raw_SpeedLimit: Optional[str] = None
    raw_LowbatLimit: Optional[str] = None


    model_config = {
        "collection": "analytics_data",
    }
