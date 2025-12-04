# app/controllers/AnalyticsDataController.py
from bson import ObjectId
from fastapi import Request
from app.models import get_db
from fastapi.responses import JSONResponse
from app.helpers.ErrorCodes import ErrorCodes
from app.models.AnalyticsData import AnalyticsData
from app.controllers.APIResponse import APIResponse


def normalize_processed_at(val):
    if val is None:
        return None
    if isinstance(val, dict) and "$date" in val:
        return val["$date"]
    if hasattr(val, "isoformat"):
        return val.isoformat()
    return str(val)

def serialize(record):
    d = record.dict() if hasattr(record, "dict") else dict(record)

    # handle _id → string
    _id = d.get("_id") or d.get("id")
    if isinstance(_id, dict) and "$oid" in _id:
        d["id"] = _id["$oid"]
    elif isinstance(_id, ObjectId):
        d["id"] = str(_id)

    # map mixed-case fields
    d["geoid"] = d.get("geoid") or d.get("Geoid")
    d["battery"] = d.get("battery") or d.get("Battery")
    d["signal"] = d.get("signal") or d.get("Signal")
    d["alert"] = d.get("alert") or d.get("Alert")

    d["processed_at"] = normalize_processed_at(d.get("processed_at"))

    # convert created_at if exists
    if d.get("created_at") and hasattr(d["created_at"], "isoformat"):
        d["created_at"] = d["created_at"].isoformat()

    return {
        "id": d.get("id"),
        "topic": d.get("topic"),
        "imei": d.get("imei"),
        "interval": d.get("interval"),
        "geoid": d.get("geoid"),
        "packet": d.get("packet"),
        "latitude": d.get("latitude"),
        "longitude": d.get("longitude"),
        "speed": d.get("speed"),
        "battery": d.get("battery"),
        "signal": d.get("signal"),
        "alert": d.get("alert"),
        "raw_text": d.get("raw_text"),
        "timestamp_normalized": d.get("timestamp_normalized"),
        "timestamp_iso": d.get("timestamp_iso"),
        "timestamp": d.get("timestamp"),
        "received_at_ist": d.get("received_at_ist"),
        "processed_at": d.get("processed_at"),
        "type": d.get("type"),
        "created_at": d.get("created_at"),
    }

class AnalyticsDataController:

    async def all(self, request: Request):
        db = get_db()
        recs = await db.find(AnalyticsData, {})
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
        recs = await db.find(AnalyticsData, {})
        sliced = recs[skip: skip + limit]
        return JSONResponse(APIResponse.success("ok", [serialize(r) for r in sliced]))

    async def count(self, request: Request):
        db = get_db()
        c = await db.count(AnalyticsData)
        return JSONResponse(APIResponse.success("ok", {"count": c}))
