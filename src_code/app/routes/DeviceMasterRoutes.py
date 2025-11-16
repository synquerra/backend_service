# app/routes/DeviceMasterRoutes.py
from fastapi import Request

async def list_devices_handler(request: Request):
    from app.controllers.DeviceMasterController import DeviceMasterController
    return await DeviceMasterController().list_devices(request)

async def device_by_topic_handler(topic: str, request: Request):
    from app.controllers.DeviceMasterController import DeviceMasterController
    return await DeviceMasterController().device_by_topic(topic, request)
