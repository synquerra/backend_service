# app/controllers/CommandController.py

import json
from app.libraries.MqttConnector import mqtt_connector


class CommandController:

    @staticmethod
    def publish(topic: str, payload: dict, qos: int = 0):
        """
        Publish MQTT message to any topic.
        """
        message = json.dumps(payload)
        mqtt_connector.client.publish(topic, message, qos)

        return {
            "topic": topic,
            "payload": payload,
            "qos": qos
        }

    @staticmethod
    def stop_sos(command):
        """
        Send SOS stop command to device.
        """
        topic = f"{command.imei}/sub"
        payload = {"SOS": "Stop_SOS"}

        return CommandController.publish(topic, payload)

    @staticmethod
    def query_normal(command):
        """
        Ask device to send a normal packet immediately.
        """
        topic = f"{command.imei}/sub"
        payload = {"Query": "NormalPacket"}

        return CommandController.publish(topic, payload)

    @staticmethod
    def query_device_settings(command):
        """
        Ask device to send full device configuration settings.
        """
        topic = f"{command.imei}/sub"
        payload = {"Query": "DeviceSettings"}

        return CommandController.publish(topic, payload)
