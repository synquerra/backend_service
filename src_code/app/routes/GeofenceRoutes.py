from fastapi import APIRouter
from app.controllers.GeofenceController import GeofenceController

router = APIRouter()

@router.get("/list/{imei}")
async def get_geofence_by_imei(imei: str):
    return await GeofenceController.list_by_imei(imei)
