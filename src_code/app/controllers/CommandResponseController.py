from app.models import get_db
from app.models.AnalyticsData import AnalyticsData

class CommandResponseController:

    @staticmethod
    async def get_config_or_misc(imei: str, limit: int = 50):
        db = get_db()

        return await db.find(
            AnalyticsData,
            AnalyticsData.type == "config_or_misc",
            AnalyticsData.topic == f"{imei}/pub",
            sort=AnalyticsData.device_timestamp.desc(),
            limit=limit
        )
