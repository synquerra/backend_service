# app/constants/CommandDefinitions.py

COMMAND_DEFINITIONS = {
    # --- SOS ---
    "STOP_SOS": {
        "payload": {"SOS": "Stop_SOS"},
        "qos": 2,
        "expects_ack": True
    },

    # --- QUERY ---
    "QUERY_NORMAL": {
        "payload": {"Query": "NormalPacket"},
        "qos": 0,
        "expects_ack": True
    },
    "QUERY_DEVICE_SETTINGS": {
        "payload": {"Query": "DeviceSettings"},
        "qos": 0,
        "expects_ack": True
    },

    # --- CALL ---
    "CALL_ENABLE": {
        "payload": {"Call": "Enable"},
        "qos": 0,
        "expects_ack": False
    },
    "CALL_DISABLE": {
        "payload": {"Call": "Disable"},
        "qos": 0,
        "expects_ack": False
    },

    # --- LED ---
    "LED_ON": {
        "payload": {"LED": "SwitchOnLed"},
        "qos": 0,
        "expects_ack": False
    },
    "LED_OFF": {
        "payload": {"LED": "SwitchoffLed"},
        "qos": 0,
        "expects_ack": False
    },

    # --- AMBIENT LISTEN ---
    "AMBIENT_ENABLE": {
        "payload": {"AmbientListen": "Enable"},
        "qos": 0,
        "expects_ack": False
    },
    "AMBIENT_DISABLE": {
        "payload": {"AmbientListen": "Disable"},
        "qos": 0,
        "expects_ack": False
    },
    "AMBIENT_STOP": {
        "payload": {"AmbientListen": "Stop"},
        "qos": 0,
        "expects_ack": False
    },

    # --- AIRPLANE ---
    "AIRPLANE_ENABLE": {
        "payload": {"AirplaneMode": "enable"},
        "qos": 0,
        "expects_ack": False
    },

    # --- GEOFENCE ---
    "SET_GEOFENCE": {
    "payload": {},
    "qos": 0,
    "expects_ack": False
    },

}
