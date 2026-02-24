from fastapi import APIRouter, Query
from app.controllers.CommandSentController import CommandSentController

router = APIRouter()

# 🔹 Get all commands for an IMEI
@router.get("/{imei}")
async def get_commands(
    imei: str,
    limit: int = Query(5, le=1000)
):
    return await CommandSentController.list_by_imei(imei, limit)


# 🔹 Get latest command for an IMEI
@router.get("/{imei}/latest")
async def get_latest_command(imei: str):
    return await CommandSentController.latest_by_imei(imei)
