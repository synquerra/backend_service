from fastapi import APIRouter
from app.models.CommandRequest import CommandRequest
from app.controllers.CommandController import CommandController

router = APIRouter()

@router.post("/send")
async def send_command(command: CommandRequest):
    return await CommandController.send(command)
