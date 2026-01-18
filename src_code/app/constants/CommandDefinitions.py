# app/constants/CommandDefinitions.py

COMMAND_DEFINITIONS = {

    # ---------- SOS ----------
    "STOP_SOS": {
        "payload": {"SOS": "Stop_SOS"},
        "qos": 2
    },

    # ---------- QUERY ----------
    "QUERY_NORMAL": {
        "payload": {"Query": "NormalPacket"},
        "qos": 0
    },
    "QUERY_DEVICE_SETTINGS": {
        "payload": {"Query": "DeviceSettings"},
        "qos": 0
    },

    # ---------- GEOFENCE ----------
    "SET_GEOFENCE": {
        "payload": {},
        "qos": 2
    },

    # ---------- CONTACTS ----------
    "SET_CONTACTS": {
        "payload": {},
        "qos": 2
    },

    # ---------- DEVICE SETTINGS ----------
    "DEVICE_SETTINGS": {
        "payload": {},
        "qos": 2
    },

    # ---------- CALL ----------
    "CALL_ENABLE": {
        "payload": {"Call": "Enable"},
        "qos": 2
    },
    "CALL_DISABLE": {
        "payload": {"Call": "Disable"},
        "qos": 2
    },

    # ---------- LED ----------
    "LED_ON": {
        "payload": {"LED": "SwitchOnLed"},
        "qos": 2
    },
    "LED_OFF": {
        "payload": {"LED": "SwitchoffLed"},
        "qos": 2
    },

    # ---------- AMBIENT ----------
    "AMBIENT_ENABLE": {
        "payload": {"AmbientListen": "Enable"},
        "qos": 2
    },
    "AMBIENT_DISABLE": {
        "payload": {"AmbientListen": "Disable"},
        "qos": 2
    },
    "AMBIENT_STOP": {
        "payload": {"AmbientListen": "Stop"},
        "qos": 2
    },

    # ---------- AIRPLANE ----------
    "AIRPLANE_ENABLE": {
        "payload": {"AirplaneMode": "enable"},
        "qos": 2
    },

    # ---------- GPS ----------
    "GPS_DISABLE": {
        "payload": {"NormalSendingInterval": "0"},
        "qos": 2
    },

    # ---------- FOTA ----------
    "FOTA_UPDATE": {
        "payload": {},
        "qos": 2
    }
}
