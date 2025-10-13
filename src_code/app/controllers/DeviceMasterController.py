from bson import ObjectId
from datetime import datetime
from app.models import get_db
from fastapi.responses import JSONResponse
from app.helpers.ErrorCodes import ErrorCodes
from app.models.DeviceMaster import DeviceMaster
from app.controllers.APIResponse import APIResponse
from app.helpers.ErrorMessages import ErrorMessages

class DeviceMasterController:
    @staticmethod
    def serialize_document(doc: dict, object_id: ObjectId) -> dict:
        doc.pop("id", None)
        serialized = {}
        for key, value in doc.items():
            if isinstance(value, ObjectId):
                serialized[key] = str(value)
            elif isinstance(value, datetime):
                serialized[key] = value.isoformat()
            else:
                serialized[key] = value
        serialized["_id"] = str(object_id)
        return serialized

    async def get_device_by_id(self, device_unique_id: str):
        db = get_db()
        try:
            device = await db.find_one(DeviceMaster, {"device_unique_id": device_unique_id})
            if not device:
                return JSONResponse(
                    content=APIResponse.error(msg="Device not found", code=ErrorCodes.NOT_FOUND),
                    status_code=ErrorCodes.NOT_FOUND
                )
            device_data = self.serialize_document(device.dict(), device.id)
            return JSONResponse(
                content=APIResponse.success(msg="Device found", data=device_data),
                status_code=ErrorCodes.SUCCESS
            )
        except Exception as e:
            return JSONResponse(
                content=APIResponse.error(msg=f"Error: {str(e)}", code=ErrorCodes.INTERNAL_SERVER_ERROR),
                status_code=ErrorCodes.INTERNAL_SERVER_ERROR
            )

    async def list_devices_paginated(self, page: int = 1, limit: int = 10):
        db = get_db()
        try:
            skip = (page - 1) * limit
            devices = await db.find(DeviceMaster, skip=skip, limit=limit)
            total = await db.count(DeviceMaster)
            serialized_devices = [self.serialize_document(d.dict(), d.id) for d in devices]
            return JSONResponse(
                content=APIResponse.success(msg="Devices fetched", data={
                    "total": total,
                    "page": page,
                    "limit": limit,
                    "devices": serialized_devices
                }),
                status_code=ErrorCodes.SUCCESS
            )
        except Exception as e:
            return JSONResponse(
                content=APIResponse.error(msg=f"Error: {str(e)}", code=ErrorCodes.INTERNAL_SERVER_ERROR),
                status_code=ErrorCodes.INTERNAL_SERVER_ERROR
            )
