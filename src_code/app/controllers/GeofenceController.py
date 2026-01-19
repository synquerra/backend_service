from app.models import get_db
from app.models.GeofenceData import GeofenceData


class GeofenceController:

    @staticmethod
    async def list_by_imei(imei: str):
        db = get_db()

        geofences = await db.find(
            GeofenceData,
            GeofenceData.imei == imei,
            sort=GeofenceData.created_at
        )

        # ALWAYS return a list
        return {
            "imei": imei,
            "count": len(geofences),
            "data": geofences
        }
