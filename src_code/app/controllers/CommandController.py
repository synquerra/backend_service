# app/controllers/CommandController.py

import json
from datetime import datetime
from fastapi import HTTPException

from app.models import get_db
from app.models.DeviceCommand import DeviceCommand
from app.libraries.MqttConnector import mqtt_connector
from app.constants.CommandDefinitions import COMMAND_DEFINITIONS


class CommandController:

    @staticmethod
    async def send(command_req):
        """
        Unified command dispatcher.
        Enforces firmware rules before publishing to MQTT.
        """

        # -------------------------------------------------
        # 1. Validate command
        # -------------------------------------------------
        if command_req.command not in COMMAND_DEFINITIONS:
            raise HTTPException(
                status_code=400,
                detail=f"Unsupported command: {command_req.command}"
            )

        definition = COMMAND_DEFINITIONS[command_req.command]

        # -------------------------------------------------
        # 2. Command-specific validation
        # -------------------------------------------------

        # ---- GEOFENCE ----
        if command_req.command == "SET_GEOFENCE":
            geo = command_req.params.get("geofence_number")
            coords = command_req.params.get("coordinates")

            if geo not in {"GEO1", "GEO2", "GEO3"}:
                raise HTTPException(
                    400,
                    "Invalid geofence_number (GEO1, GEO2, GEO3 only)"
                )

            if not isinstance(coords, list) or len(coords) != 5:
                raise HTTPException(
                    400,
                    "Firmware requires exactly 5 coordinates per geofence"
                )

            for i, p in enumerate(coords):
                if "latitude" not in p or "longitude" not in p:
                    raise HTTPException(
                        400,
                        f"Invalid coordinate at index {i}"
                    )

        # ---- CONTACTS ----
        if command_req.command == "SET_CONTACTS":
            for k in ("phonenum1", "phonenum2", "controlroomnum"):
                v = command_req.params.get(k)
                if not v or not str(v).isdigit():
                    raise HTTPException(
                        400,
                        f"{k} must be numeric"
                    )

        # ---- DEVICE SETTINGS ----
        if command_req.command == "DEVICE_SETTINGS":
            required = {
                "NormalSendingInterval",
                "SOSSendingInterval",
                "NormalScanningInterval",
                "AirplaneInterval",
                "TemperatureLimit",
                "SpeedLimit",
                "LowbatLimit"
            }
            missing = required - command_req.params.keys()
            if missing:
                raise HTTPException(
                    400,
                    f"Missing fields: {', '.join(missing)}"
                )

        # ---- FOTA ----
        if command_req.command == "FOTA_UPDATE":
            for k in ("FOTA", "CRC", "size", "vc"):
                if k not in command_req.params:
                    raise HTTPException(
                        400,
                        f"Missing FOTA field: {k}"
                    )

        # -------------------------------------------------
        # 3. Build payload
        # -------------------------------------------------
        payload = definition["payload"].copy()
        payload.update(command_req.params)

        topic = f"{command_req.imei}/sub"
        qos = definition["qos"]

        # -------------------------------------------------
        # 4. Publish MQTT
        # -------------------------------------------------
        try:
            mqtt_connector.client.publish(
                topic,
                json.dumps(payload),
                qos
            )
        except Exception as e:
            raise HTTPException(
                500,
                f"MQTT publish failed: {str(e)}"
            )

        # -------------------------------------------------
        # 5. Persist command
        # -------------------------------------------------
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

        # -------------------------------------------------
        # 6. API response
        # -------------------------------------------------
        return {
            "message": (
                "Command sent successfully (no device ACK expected)"
                if not definition["expects_ack"]
                else "Command sent successfully"
            ),
            "imei": command_req.imei,
            "command": command_req.command,
            "payload": payload,
            "qos": qos
        }
