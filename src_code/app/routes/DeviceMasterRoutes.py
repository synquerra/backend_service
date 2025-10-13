from app.controllers.DeviceMasterController import DeviceMasterController

controller = DeviceMasterController()

async def get_device(device_unique_id: str):
    return await controller.get_device_by_id(device_unique_id)

async def list_devices(page: int = 1, limit: int = 10):
    return await controller.list_devices_paginated(page=page, limit=limit)
