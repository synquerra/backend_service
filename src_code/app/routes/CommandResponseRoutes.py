from fastapi import APIRouter, Query
from app.controllers.CommandResponseController import CommandResponseController

router = APIRouter()

@router.get("/{imei}/config-or-misc")
async def get_config_or_misc(imei: str, limit: int = Query(5, le=1000)):
    return await CommandResponseController.get_config_or_misc(imei=imei,  limit=limit)
