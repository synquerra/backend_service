# app/libraries/MqttConnector.py

import paho.mqtt.client as mqtt
from app.config.config import settings

class MqttConnector:
    def __init__(self):
        self.client = mqtt.Client()

        if settings.MQTT_USERNAME and settings.MQTT_PASSWORD:
            self.client.username_pw_set(settings.MQTT_USERNAME, settings.MQTT_PASSWORD)

        self.client.connect(settings.MQTT_BROKER, settings.MQTT_PORT, 60)

mqtt_connector = MqttConnector()
