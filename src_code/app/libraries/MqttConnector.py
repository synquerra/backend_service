# app/libraries/MqttConnector.py

import paho.mqtt.client as mqtt
from app.config.config import settings
import logging

logger = logging.getLogger(__name__)

class MqttConnector:
    def __init__(self):
        self.client = mqtt.Client(client_id=f"api-{settings.APP_NAME}", clean_session=True)

        if settings.MQTT_USERNAME and settings.MQTT_PASSWORD:
            self.client.username_pw_set(settings.MQTT_USERNAME, settings.MQTT_PASSWORD)

        self.client.on_connect = self.on_connect
        self.client.on_disconnect = self.on_disconnect

        self.client.connect(settings.MQTT_BROKER, settings.MQTT_PORT, keepalive=60)

        self.client.loop_start()

    def on_connect(self, client, userdata, flags, rc):
        logger.info(f"MQTT connected with rc={rc}")

    def on_disconnect(self, client, userdata, rc):
        logger.error(f"MQTT disconnected rc={rc}")

mqtt_connector = MqttConnector()
