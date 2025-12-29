# app/workers/MqttResponseHandler.py

from datetime import datetime
from app.models import get_db
from app.models.DeviceCommand import DeviceCommand


async def handle_device_message(imei: str, payload: dict):
    """
    Called when a message is received on {imei}/pub
    """
    db = get_db()

    # Find last pending command
    cmd = await db.find_one(
        DeviceCommand,
        DeviceCommand.imei == imei,
        DeviceCommand.status == "SENT"
    )

    if cmd:
        cmd.status = "DELIVERED"
        cmd.updated_at = datetime.utcnow()
        await db.save(cmd)
