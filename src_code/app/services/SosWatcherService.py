from app.models import engine
from app.websocket.ConnectionManager import manager
from app.models.AnalyticsData import AnalyticsData


async def watch_sos_events():

    collection = engine.get_collection(AnalyticsData)

    pipeline = [
        {"$match": {"operationType": "insert"}}
    ]

    async with collection.watch(pipeline) as stream:

        async for change in stream:

            data = change["fullDocument"]

            alert = data.get("Alert")
            sos_disabled = data.get("sos_disabled", False)

            if alert == "A1002" and sos_disabled is not True:

                payload = {
                    "event": "SOS_ALERT",
                    "imei": data.get("imei"),
                    "alert": alert,
                    "timestamp": str(data.get("device_timestamp"))
                }

                await manager.broadcast(payload)