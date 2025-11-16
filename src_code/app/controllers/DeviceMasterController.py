# app/controllers/DeviceMasterController.py
from fastapi import Request
from fastapi.responses import JSONResponse
from app.models import get_db
from datetime import datetime
from app.models.DeviceMaster import DeviceMaster
from app.controllers.APIResponse import APIResponse
from app.helpers.ErrorCodes import ErrorCodes

def serialize_device(record):
    if not record:
        return None

    data = record.dict()

    created = data.get("created_at")

    if isinstance(created, datetime):
        created_stripped = created.strftime("%Y-%m-%d %H:%M:%S")
    elif isinstance(created, str):
        created_stripped = created.split(".")[0]
    else:
        created_stripped = None

    return {
        "topic": data.get("topic"),
        "imei": data.get("imei"),
        "interval": data.get("interval"),
        "geoid": data.get("Geoid"),
        "createdAt": created_stripped,
    }


class DeviceMasterController:

    async def list_devices(self, request: Request):
        try:
            db = get_db()
            records = await db.find(DeviceMaster, {})

            devices = [serialize_device(r) for r in records]

            return JSONResponse(
                APIResponse.success(
                    msg="Device list fetched successfully",
                    data=devices
                ),
                status_code=ErrorCodes.SUCCESS
            )

        except Exception as e:
            return JSONResponse(
                APIResponse.error(
                    msg=f"Unexpected error: {str(e)}",
                    code=ErrorCodes.INTERNAL_SERVER_ERROR
                ),
                status_code=ErrorCodes.INTERNAL_SERVER_ERROR
            )


    async def device_by_topic(self, topic: str, request: Request):
        try:
            db = get_db()
            record = await db.find_one(DeviceMaster, {"topic": topic})

            if not record:
                return JSONResponse(
                    APIResponse.error(
                        msg="Device not found",
                        code=ErrorCodes.NOT_FOUND
                    ),
                    status_code=ErrorCodes.NOT_FOUND
                )

            return JSONResponse(
                APIResponse.success(
                    msg="Device fetched successfully",
                    data=serialize_device(record)
                ),
                status_code=ErrorCodes.SUCCESS
            )

        except Exception as e:
            return JSONResponse(
                APIResponse.error(
                    msg=f"Unexpected error: {str(e)}",
                    code=ErrorCodes.INTERNAL_SERVER_ERROR
                ),
                status_code=ErrorCodes.INTERNAL_SERVER_ERROR
            )
