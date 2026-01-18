# app/controllers/CommandController.py

import json
from app.models import get_db
from zoneinfo import ZoneInfo
from datetime import datetime, timezone
from fastapi import HTTPException
from app.models.DeviceCommand import DeviceCommand
from app.libraries.MqttConnector import mqtt_connector
from app.constants.CommandDefinitions import COMMAND_DEFINITIONS

IST = ZoneInfo("Asia/Kolkata")

class CommandController:

    @staticmethod
    async def send(command_req):

        if command_req.command not in COMMAND_DEFINITIONS:
            raise HTTPException(400, "Unsupported command")

        definition = COMMAND_DEFINITIONS[command_req.command]

        # STRICT validation for SET_CONTACTS (firmware page 2)
        if command_req.command == "SET_CONTACTS":
            for k in ("phonenum1", "phonenum2", "controlroomnum"):
                v = command_req.params.get(k)
                if not v or not str(v).isdigit():
                    raise HTTPException(400, f"{k} must be numeric")

        payload = {**definition["payload"], **command_req.params}

        topic = f"{command_req.imei}/sub"
        qos = definition["qos"]

        result = mqtt_connector.client.publish(
            topic,
            json.dumps(payload),
            qos=qos
        )

        if result.rc != 0:
            raise HTTPException(500, "MQTT publish failed")

        created_at_ist = (
            datetime.now(timezone.utc)
            .astimezone(IST)
            .replace(tzinfo=None)
        )

        db = get_db()
        await db.save(DeviceCommand(
            imei=command_req.imei,
            command=command_req.command,
            payload=payload,
            qos=qos,
            status="PUBLISHED",  # NOT DELIVERED
            created_at=created_at_ist,
            updated_at=None
        ))

        return {
            "status": "SENT",
            "note": "Command published to broker; device execution not confirmed",
            "imei": command_req.imei,
            "command": command_req.command,
            "qos": qos,
            "created_at": created_at_ist.isoformat()
        }
