from app.models import get_db
from fastapi import HTTPException
from app.models.DeviceCommand import DeviceCommand


class CommandSentController:

    @staticmethod
    async def list_by_imei(imei: str, limit: int = 1000):
        db = get_db()

        return await db.find(
            DeviceCommand,
            DeviceCommand.imei == imei,
            sort=DeviceCommand.created_at.desc(),
            limit=limit
        )

    @staticmethod
    async def latest_by_imei(imei: str):
        db = get_db()

        command = await db.find_one(
            DeviceCommand,
            DeviceCommand.imei == imei,
            sort=DeviceCommand.created_at.desc()
        )

        if not command:
            raise HTTPException(404, "No command found")

        return command
