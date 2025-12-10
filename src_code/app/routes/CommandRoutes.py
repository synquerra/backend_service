# app/routes/CommandRoutes.py

from fastapi import APIRouter
from app.models.CommandModel import CommandModel
from app.controllers.CommandController import CommandController

router = APIRouter(prefix="/command", tags=["Command"])


@router.post("/stop-sos")
def stop_sos(command: CommandModel):
    result = CommandController.stop_sos(command)

    return {
        "message": "SOS stop command sent",
        **result
    }


@router.post("/normal_query")
def query_device(command: CommandModel):
    result = CommandController.query_normal(command)

    return {
        "message": "Normal packet query sent",
        **result
    }

@router.post("/device-settings")
def query_device_settings(command: CommandModel):
    result = CommandController.query_device_settings(command)

    return {
        "message": "Device settings query sent",
        **result
    }
