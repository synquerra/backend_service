# app/controllers/AnalyticsDataController.py
from fastapi import Request
from fastapi.responses import JSONResponse
from bson import ObjectId
from dateutil import parser
from typing import Any

from app.models import get_db
from app.models.AnalyticsData import AnalyticsData
from app.controllers.APIResponse import APIResponse

def parse_date(v: Any):
    if not v:
        return None
    # If it's already a datetime, return isoformat
    try:
        if hasattr(v, "isoformat"):
            return v.isoformat()
        return parser.parse(str(v)).isoformat()
    except:
        return str(v)

def serialize(rec: AnalyticsData):
    # rec is an ODMantic model instance
    d = rec.dict()

    # Convert _id → string (ODMantic uses 'id' attribute)
    d["id"] = str(d.get("id") or d.get("_id") or "")
    d.pop("_id", None)

    # Use device_timestamp (datetime) as canonical sorting/display timestamp
    device_ts = d.get("device_timestamp")  # this is a datetime object (tz-aware) or None

    return {
        "id": d.get("id"),
        "topic": d.get("topic"),
        "imei": d.get("imei"),
        "interval": d.get("interval"),

        "geoid": d.get("Geoid"),
        "packet": d.get("packet"),
        "latitude": d.get("latitude"),
        "longitude": d.get("longitude"),
        "speed": d.get("speed"),

        "battery": d.get("Battery"),
        "signal": d.get("Signal"),
        "alert": d.get("Alert"),

        # UI HEADER → ALWAYS device_timestamp (server IST time) in ISO
        "deviceTimestamp": parse_date(device_ts),

        # device raw timestamp (string as device sent)
        "deviceRawTimestamp": d.get("device_raw_timestamp"),

        # UI LIST SORTING → using device_timestamp as the canonical sortable timestamp
        "timestamp": parse_date(device_ts),

        # RAW flattened fields (camelCase)
        "rawPacket": d.get("raw_packet"),
        "rawImei": d.get("raw_imei"),
        "rawAlert": d.get("raw_Alert"),
        "rawTemperature": d.get("raw_temperature"),
        "rawSpeed": d.get("raw_speed"),
        "rawSignal": d.get("raw_Signal"),
        "rawBattery": d.get("raw_Battery"),
        "rawGeoid": d.get("raw_Geoid"),
        "rawLatitude": d.get("raw_latitude"),
        "rawLongitude": d.get("raw_longitude"),
        "rawInterval": d.get("raw_interval"),
        "rawBody": d.get("raw_body"),
        "rawPhone1": d.get("raw_phonenum1"),
        "rawPhone2": d.get("raw_phonenum2"),
        "rawControlPhone": d.get("raw_controlroomnum"),
        "rawNormalSendingInterval": d.get("raw_NormalSendingInterval"),
        "rawSOSSendingInterval": d.get("raw_SOSSendingInterval"),
        "rawNormalScanningInterval": d.get("raw_NormalScanningInterval"),
        "rawAirplaneInterval": d.get("raw_AirplaneInterval"),
        "rawSpeedLimit": d.get("raw_SpeedLimit"),
        "rawLowbatLimit": d.get("raw_LowbatLimit"),
        "type": d.get("type"),
    }

class AnalyticsDataController:

    async def all(self, request: Request):
        db = get_db()
        recs = await db.find(AnalyticsData)
        return JSONResponse(APIResponse.success("ok", [serialize(r) for r in recs]))

    async def by_id(self, id: str, request: Request):
        db = get_db()
        try:
            rec = await db.find_one(AnalyticsData, {"_id": ObjectId(id)})
        except:
            return JSONResponse(APIResponse.error("Invalid ID", 400), 400)

        if not rec:
            return JSONResponse(APIResponse.error("Not found", 404), 404)

        return JSONResponse(APIResponse.success("ok", serialize(rec)))

    async def by_topic(self, topic: str, request: Request):
        db = get_db()
        recs = await db.find(AnalyticsData, {"topic": topic})
        return JSONResponse(APIResponse.success("ok", [serialize(r) for r in recs]))

    async def by_imei(self, imei: str, request: Request):
        db = get_db()
        recs = await db.find(AnalyticsData, {"imei": imei})
        return JSONResponse(APIResponse.success("ok", [serialize(r) for r in recs]))

    async def paginated(self, skip: int, limit: int, request: Request):
        db = get_db()
        recs = await db.find(AnalyticsData)
        sliced = recs[skip:skip + limit]
        return JSONResponse(APIResponse.success("ok", [serialize(r) for r in sliced]))

    async def count(self, request: Request):
        db = get_db()
        count = await db.count(AnalyticsData)
        return JSONResponse(APIResponse.success("ok", {"count": count}))
