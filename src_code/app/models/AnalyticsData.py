# app/models/AnalyticsData.py
from odmantic import Model, Field
from datetime import datetime, timedelta
from typing import Optional, Any

def now_ist():
    return datetime.utcnow() + timedelta(hours=5, minutes=30)

class AnalyticsData(Model):
    topic: Optional[str] = None
    imei: Optional[str] = None
    interval: Optional[int] = None
    geoid: Optional[str] = None          # maps Geoid
    packet: Optional[str] = None
    latitude: Optional[str] = None
    longitude: Optional[str] = None
    speed: Optional[str] = None
    battery: Optional[str] = None        # maps Battery
    signal: Optional[str] = None         # maps Signal
    alert: Optional[str] = None          # maps Alert
    raw_text: Optional[str] = None

    timestamp_normalized: Optional[str] = None
    timestamp_iso: Optional[str] = None
    timestamp: Optional[str] = None

    received_at_ist: Optional[str] = None
    processed_at: Optional[Any] = None   # can be $date dict or datetime

    type: Optional[str] = None

    model_config = {
        "collection": "analytics_data"
    }
