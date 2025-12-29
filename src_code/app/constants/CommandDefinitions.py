# app/constants/CommandDefinitions.py

COMMAND_DEFINITIONS = {

    # ---------- SOS ----------
    "STOP_SOS": {
        "payload": {"SOS": "Stop_SOS"},
        "qos": 2,
        "expects_ack": True
    },

    # ---------- QUERY ----------
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

    # ---------- GEOFENCE ----------
    "SET_GEOFENCE": {
        "payload": {},          # full payload from params
        "qos": 0,
        "expects_ack": False
    },

    # ---------- CONTACTS ----------
    "SET_CONTACTS": {
        "payload": {},          # full payload from params
        "qos": 0,
        "expects_ack": False
    },

    # ---------- DEVICE SETTINGS ----------
    "DEVICE_SETTINGS": {
        "payload": {},          # intervals & thresholds
        "qos": 0,
        "expects_ack": False
    },

    # ---------- CALL ----------
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

    # ---------- LED ----------
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

    # ---------- AMBIENT LISTEN ----------
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

    # ---------- AIRPLANE ----------
    "AIRPLANE_ENABLE": {
        "payload": {"AirplaneMode": "enable"},
        "qos": 0,
        "expects_ack": False
    },

    # ---------- GPS ----------
    "GPS_DISABLE": {
        "payload": {"NormalSendingInterval": "0"},
        "qos": 0,
        "expects_ack": False
    },

    # ---------- FOTA ----------
    "FOTA_UPDATE": {
        "payload": {},          # FOTA, CRC, size, vc from params
        "qos": 2,
        "expects_ack": True
    }
}
