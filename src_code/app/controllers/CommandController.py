import json
from app.models import get_db
from datetime import datetime
from fastapi import HTTPException
from app.models.DeviceCommand import DeviceCommand
from app.libraries.MqttConnector import mqtt_connector
from app.constants.CommandDefinitions import COMMAND_DEFINITIONS


class CommandController:

    @staticmethod
    async def send(command_req):
        # 1. Validate command
        if command_req.command not in COMMAND_DEFINITIONS:
            raise HTTPException(
                status_code=400,
                detail=f"Unsupported command: {command_req.command}"
            )

        definition = COMMAND_DEFINITIONS[command_req.command]

        # 2. Command-specific validation
        if command_req.command == "SET_CONTACTS":
            for k in ("phonenum1", "phonenum2", "controlroomnum"):
                v = command_req.params.get(k)
                if not v or not str(v).isdigit():
                    raise HTTPException(400, f"{k} must be numeric")

        # 3. Build payload (SAFE)
        payload = dict(definition["payload"])
        for k, v in command_req.params.items():
            payload[k] = v

        topic = f"{command_req.imei}/sub"
        qos = definition["qos"]

        # 4. Publish MQTT
        try:
            mqtt_connector.client.publish(
                topic,
                json.dumps(payload),
                qos=qos
            )
        except Exception as e:
            raise HTTPException(500, f"MQTT publish failed: {e}")

        # 5. Persist command
        db = get_db()
        cmd = DeviceCommand(
            imei=command_req.imei,
            command=command_req.command,
            payload=payload,
            qos=qos,
            status="SENT",
            created_at=datetime.utcnow()
        )
        await db.save(cmd)

        # 6. Response
        return {
            "message": "Command sent successfully",
            "imei": command_req.imei,
            "command": command_req.command,
            "payload": payload,
            "qos": qos
        }
