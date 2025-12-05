from fastapi import Request
from fastapi.responses import JSONResponse
from bson import ObjectId
from dateutil import parser

from app.models import get_db
from app.models.AnalyticsData import AnalyticsData
from app.controllers.APIResponse import APIResponse


def parse_date(v):
    if not v:
        return None
    try:
        return parser.parse(str(v)).isoformat()
    except:
        return str(v)


def serialize(rec):
    d = rec.dict()

    # Convert _id → string
    d["id"] = str(rec.id)
    d.pop("_id", None)

    # HEADER TIMESTAMP (always device_timestamp)
    device_ts = d.get("device_timestamp")

    # SORTING TIMESTAMP (fallback allowed)
    sorting_ts = (
        d.get("device_timestamp")
        or d.get("raw_timestamp")
        or d.get("received_at_utc")
    )

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

        # UI HEADER → ALWAYS device_timestamp
        "deviceTimestamp": parse_date(device_ts),

        # Display raw UTC (if needed)
        "receivedAtUtc": parse_date(d.get("received_at_utc")),

        # UI LIST SORTING → best available timestamp
        "timestamp": parse_date(sorting_ts),

        # RAW fields
        "rawTimestamp": parse_date(d.get("raw_timestamp")),
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
