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
        """
        Unified command dispatcher for all device commands.
        Enforces firmware-level validation before publishing to MQTT.
        """

        # 1. Validate command existence
        if command_req.command not in COMMAND_DEFINITIONS:
            raise HTTPException(
                status_code=400,
                detail=f"Unsupported command: {command_req.command}"
            )

        definition = COMMAND_DEFINITIONS[command_req.command]

        # 2. Command-specific validation

        # ---- GEOFENCE VALIDATION ----
        if command_req.command == "SET_GEOFENCE":
            geo = command_req.params.get("geofence_number")
            geo_id = command_req.params.get("geofence_id")
            coords = command_req.params.get("coordinates")

            if geo not in {"GEO1", "GEO2", "GEO3"}:
                raise HTTPException(
                    status_code=400,
                    detail="Invalid geofence_number. Allowed values: GEO1, GEO2, GEO3"
                )

            if not isinstance(coords, list):
                raise HTTPException(
                    status_code=400,
                    detail="coordinates must be a list"
                )

            if len(coords) != 5:
                raise HTTPException(
                    status_code=400,
                    detail="Firmware requires exactly 5 coordinates per geofence"
                )

            for idx, point in enumerate(coords):
                if not isinstance(point, dict):
                    raise HTTPException(
                        status_code=400,
                        detail=f"Invalid coordinate format at index {idx}"
                    )

                if "latitude" not in point or "longitude" not in point:
                    raise HTTPException(
                        status_code=400,
                        detail=f"Coordinate at index {idx} must contain latitude and longitude"
                    )

        # ---- CONTACTS VALIDATION ----
        if command_req.command == "SET_CONTACTS":
            for field in ("phonenum1", "phonenum2", "controlroomnum"):
                val = command_req.params.get(field)
                if not val or not str(val).isdigit():
                    raise HTTPException(
                        status_code=400,
                        detail=f"{field} must be a numeric string"
                    )

        # ---- DEVICE SETTINGS VALIDATION ----
        if command_req.command == "DEVICE_SETTINGS":
            required_fields = {
                "NormalSendingInterval",
                "SOSSendingInterval",
                "NormalScanningInterval",
                "AirplaneInterval",
                "TemperatureLimit",
                "SpeedLimit",
                "LowbatLimit"
            }

            missing = required_fields - command_req.params.keys()
            if missing:
                raise HTTPException(
                    status_code=400,
                    detail=f"Missing device setting fields: {', '.join(missing)}"
                )

        # 3. Build MQTT payload
        payload = definition["payload"].copy()
        payload.update(command_req.params)

        topic = f"{command_req.imei}/sub"
        qos = definition["qos"]

        # 4. Publish to MQTT
        try:
            mqtt_connector.client.publish(
                topic,
                json.dumps(payload),
                qos
            )
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"MQTT publish failed: {str(e)}"
            )

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

        # 6. API Response
        return {
            "message": (
                "Command sent successfully "
                "(no device ACK expected for this command)"
                if not definition.get("expects_ack")
                else "Command sent successfully"
            ),
            "imei": command_req.imei,
            "command": command_req.command,
            "payload": payload,
            "qos": qos
        }
