from odmantic import Model
from typing import Optional, Any


class AnalyticsData(Model):
    topic: Optional[str] = None
    imei: Optional[str] = None
    interval: Optional[int] = None

    Geoid: Optional[str] = None
    packet: Optional[str] = None

    latitude: Optional[str] = None
    longitude: Optional[str] = None
    speed: Optional[int] = None

    Battery: Optional[str] = None
    Signal: Optional[str] = None
    Alert: Optional[str] = None

    device_timestamp: Optional[Any] = None
    received_at_utc: Optional[Any] = None

    type: Optional[str] = None

    raw_packet: Optional[str] = None
    raw_imei: Optional[str] = None
    raw_Alert: Optional[str] = None
    raw_timestamp: Optional[str] = None
    raw_latitude: Optional[str] = None
    raw_longitude: Optional[str] = None
    raw_speed: Optional[str] = None
    raw_temperature: Optional[str] = None
    raw_Battery: Optional[str] = None
    raw_Signal: Optional[str] = None
    raw_interval: Optional[str] = None
    raw_Geoid: Optional[str] = None

    model_config = {
        "collection": "analytics_data",
    }
