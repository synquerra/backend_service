# app/libraries/MqttConnector.py

import uuid
import logging
import paho.mqtt.client as mqtt
from app.config.config import settings

logger = logging.getLogger(__name__)

class MqttConnector:
    def __init__(self):
        client_id = f"api-{settings.APP_NAME}-{uuid.uuid4().hex}"
        self.client = mqtt.Client(client_id=client_id, clean_session=True)

        if settings.MQTT_USERNAME and settings.MQTT_PASSWORD:
            self.client.username_pw_set(settings.MQTT_USERNAME, settings.MQTT_PASSWORD)

        self.client.on_connect = self.on_connect
        self.client.on_disconnect = self.on_disconnect

        self.client.connect(settings.MQTT_BROKER, settings.MQTT_PORT, keepalive=60)

        self.client.loop_start()

        logger.info("MQTT client started client_id=%s", client_id)

    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            logger.info("MQTT connected successfully")
        else:
            logger.error("MQTT connect failed rc=%s", rc)

    def on_disconnect(self, client, userdata, rc):
        logger.error("MQTT disconnected rc=%s", rc)

mqtt_connector = MqttConnector()
