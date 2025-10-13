import json
import strawberry
from typing import List
from strawberry.exceptions import GraphQLError
from app.helpers.ErrorCodes import ErrorCodes
from app.routes.DeviceMasterRoutes import get_device, list_devices


@strawberry.type
class DeviceType:
    _id: str = strawberry.field(name="_id")
    device_unique_id: str = strawberry.field(name="device_unique_id")
    student_unique_id: str = strawberry.field(name="student_unique_id")
    parent_unique_id: str = strawberry.field(name="parent_unique_id")
    imei: str = strawberry.field(name="imei")
    model: str = strawberry.field(name="model")
    firmware_version: str = strawberry.field(name="firmware_version")
    status: str = strawberry.field(name="status")
    assigned_date: str = strawberry.field(name="assigned_date")

@strawberry.type
class PaginatedDevices:
    total: int
    page: int
    limit: int
    devices: List[DeviceType]

@strawberry.type
class Query:
    @strawberry.field(name="get_device")
    async def get_device(self, device_unique_id: str = strawberry.argument(name="device_unique_id")) -> DeviceType:
        response = await get_device(device_unique_id)
        if response.status_code != ErrorCodes.SUCCESS:
            raise GraphQLError("Device not found")
        parsed = json.loads(response.body.decode())["data"]
        return DeviceType(**parsed)

    @strawberry.field(name="list_devices")
    async def list_devices(self, page: int = 1, limit: int = 10) -> PaginatedDevices:
        response = await list_devices(page=page, limit=limit)
        if response.status_code != ErrorCodes.SUCCESS:
            raise GraphQLError("Failed to fetch devices")
        parsed = json.loads(response.body.decode())["data"]
        devices = [DeviceType(**d) for d in parsed["devices"]]
        return PaginatedDevices(
            total=parsed["total"],
            page=parsed["page"],
            limit=parsed["limit"],
            devices=devices
        )

schema = strawberry.Schema(query=Query)
