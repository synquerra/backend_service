# app/models/GeofenceData.py

from odmantic import Model
from datetime import datetime
from typing import List, Dict

class GeofenceData(Model):
    imei: str
    geofence_number: str
    geofence_id: str
    coordinates: List[Dict[str, float]]
    created_at: datetime

    model_config = {
        "collection": "geofence_data"
    }
