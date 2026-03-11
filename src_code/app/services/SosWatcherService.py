from app.models import get_db
from app.websocket.ConnectionManager import manager
from app.models.AnalyticsData import AnalyticsData


async def watch_sos_events():

    print("SOS watcher started")

    # GET ENGINE AFTER DB INIT
    engine = get_db()

    collection = engine.get_collection(AnalyticsData)

    pipeline = [
        {
            "$match": {
                "operationType": {"$in": ["insert"]}
            }
        }
    ]

    async with collection.watch(pipeline) as stream:

        async for change in stream:

            print("Mongo change detected:", change)

            data = change.get("fullDocument")

            if not data:
                continue

            alert = data.get("Alert")
            sos_disabled = bool(data.get("sos_disabled", False))

            print("Alert value:", alert)

            if alert == "A1002" and not sos_disabled:

                payload = {
                    "event": "SOS_ALERT",
                    "imei": data.get("imei"),
                    "alert": alert,
                    "timestamp": str(data.get("device_timestamp"))
                }

                print("Sending SOS event:", payload)

                await manager.broadcast(payload)